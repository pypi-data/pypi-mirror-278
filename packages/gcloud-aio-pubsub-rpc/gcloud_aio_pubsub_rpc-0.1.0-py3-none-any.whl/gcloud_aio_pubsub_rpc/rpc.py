import asyncio
import logging
import uuid
from abc import ABC
from abc import abstractmethod
from collections.abc import AsyncIterator
from collections.abc import Callable
from typing import Any

from aiohttp import ClientSession as Session
from cachetools import TTLCache
from gcloud.aio.pubsub import PubsubMessage
from gcloud.aio.pubsub import SubscriberMessage

from .config import ACK_BATCH_SIZE
from .config import ACK_MAX_WAIT_TIME
from .config import CONSUMER_MAX_MESSAGE_REQUEST
from .config import CONSUMER_SLEEP_INTERVAL
from .config import JOB_CACHE_TTL
from .config import MAX_TTL_CACHE_SIZE
from .config import NACK_BATCH_SIZE
from .config import NACK_MAX_WAIT_TIME
from .config import PRODUCER_MAX_WAIT_TIME
from .config import PUBLISH_BATCH_SIZE
from .ordered_stream import AsyncOrderedStream
from .pubsub_clients import RetryingPublisherClient
from .pubsub_clients import RetryingSubscriberClient

logger = logging.getLogger(__name__)


# TODO Add heartbeats to everything with informative log messages
class PubSubRPCBase(ABC):
    def __init__(
            self,
            project_id: str,
            inbound_topic: str,
            outbound_topic: str) -> None:
        self.project_id = project_id
        self.publisher = RetryingPublisherClient()
        self.subscriber = RetryingSubscriberClient()
        self.host_id = uuid.uuid4()

        self.inbound_subscription: str | None = None
        self.inbound_topic = f'projects/{project_id}/topics/{inbound_topic}'
        self.outbound_topic = f'projects/{project_id}/topics/{outbound_topic}'

        self.ack_queue = asyncio.Queue()
        self.nack_queue = asyncio.Queue()

        self._consume_tasks: list[asyncio.Task] = []
        self.consumer: asyncio.Task | None = None
        self.acker: asyncio.Task | None = None
        self.nacker: asyncio.Task | None = None
        self.producer: asyncio.Task | None = None

    @abstractmethod
    async def initialize(self,
                         body: dict[str, Any] | None = None,
                         *,
                         session: Session | None = None,
                         timeout: int = 10,):

        """Pre-startup steps to configure and create an inbound subscription"""
        raise NotImplementedError

    async def __consume_on_message(self, message: SubscriberMessage) -> None:
        try:
            await self._on_message(message)
        except Exception:
            logger.exception(
                f'Adding to nack queue {message}')
            await self.nack_queue.put(message.ack_id)
        else:
            logger.info(
                f'Adding to ack queue {message}')
            await self.ack_queue.put(message.ack_id)

    def __consume_task_done(self, task: asyncio.Task) -> None:
        """Consume task cleanup callback"""
        self._consume_tasks.remove(task)

    # The client and server have very different access patterns
    async def _message_consumer(self) -> None:
        """
        Long-running worker to pull and process PubSub messages.
        """
        try:
            while True:
                start = asyncio.get_running_loop().time()
                num_tasks = len(self._consume_tasks)
                max_messages = CONSUMER_MAX_MESSAGE_REQUEST - num_tasks
                if max_messages > 0:
                    try:
                        messages = await self.subscriber.pull(
                            subscription=self.inbound_subscription,
                            max_messages=max_messages
                        )
                    except Exception:
                        logger.exception(
                            'Network error, failed to pull messages')

                    for message in messages:
                        task = asyncio.create_task(
                            self.__consume_on_message(message))
                        task.add_done_callback(self.__consume_task_done)
                        self._consume_tasks.append(task)

                now = asyncio.get_running_loop().time()
                sleep_for = max(0.01, CONSUMER_SLEEP_INTERVAL - (now - start))
                # Sleep to prevent hammering in case of empty message returns
                await asyncio.sleep(sleep_for)
        except asyncio.CancelledError:
            logger.info('Consumer worker has been cancelled')
        except Exception:
            logger.exception('An error occurred in consumer')

    async def _queue_worker(self,
                            queue: asyncio.Queue[Any],
                            queue_name: str,
                            max_wait_time: int,
                            batch_size: int,
                            on_items: Callable[[list[Any]], None]):
        """
        Long-running task to publish messages to a Pub/Sub topic
        from a queue either when the batch is full or when the max
        wait time is reached.
        """
        try:
            while True:
                messages: list[Any] = []
                start_time = asyncio.get_running_loop().time()

                logging.info(
                    f'{queue_name}.qsize()={queue.qsize()}')

                while len(messages) < batch_size:
                    now = asyncio.get_running_loop().time()
                    timeout = max(0.1, max_wait_time - (now - start_time))
                    try:
                        message = await asyncio.wait_for(
                            queue.get(),
                            timeout=timeout)
                        messages.append(message)
                    except TimeoutError:
                        break

                if messages:
                    try:
                        await on_items(messages)
                    except Exception:
                        logger.exception('Error encountered processing'
                                         f' {queue_name} messages')
                    for _ in messages:
                        queue.task_done()

        except asyncio.CancelledError:
            logger.info(f'Worker for {queue_name} is shutting down.')
        finally:
            logger.info(f'Draining the {queue_name}')
            messages: list[Any] = []
            while not queue.empty():
                logging.info('Attempting to get another message')
                try:
                    message = queue.get_nowait()
                    messages.append(message)
                    queue.task_done()
                except asyncio.QueueEmpty:
                    logger.info(f'{queue_name} has been completely drained.')
                    break
                except Exception:
                    logger.exception('Unexpected error occurred draining'
                                     f' {queue_name}')
                    break
            if messages:
                try:
                    await on_items(messages)
                except Exception:
                    logger.exception('on_items threw an error during draining')
            logger.info(f'{queue_name} drained')

    async def startup(self) -> None:

        async def ack(ack_ids: list[str]) -> None:
            try:
                await self.subscriber.acknowledge(
                    self.inbound_subscription, ack_ids)
            except Exception:
                logger.exception('Failed to ack message')

        async def nack(nack_ids: list[str]) -> None:
            try:
                await self.subscriber.modify_ack_deadline(
                    subscription=self.inbound_subscription,
                    ack_ids=nack_ids,
                    ack_deadline_seconds=0)
            except Exception:
                logger.exception('Failed to nack message')

        self.consumer = asyncio.create_task(self._message_consumer())

        logger.info('Loading new workers')
        self.acker = asyncio.create_task(self._queue_worker(
            self.ack_queue,
            'acker',
            ACK_MAX_WAIT_TIME,
            ACK_BATCH_SIZE,
            ack))
        self.nacker = asyncio.create_task(self._queue_worker(
            self.nack_queue,
            'nacker',
            NACK_MAX_WAIT_TIME,
            NACK_BATCH_SIZE,
            nack))

    @abstractmethod
    async def _on_message(self, message: SubscriberMessage) -> None:
        raise NotImplementedError

    async def cleanup(self) -> None:
        await self.subscriber.delete_subscription(
            self.inbound_subscription)

        # If I cancel all tasks, then these get double cancelled?
        if self.subscriber:
            await self.subscriber.close()

        if self.publisher:
            await self.publisher.close()


class PubSubRPCClient(PubSubRPCBase):
    def __init__(
            self,
            project_id: str,
            inbound_topic: str,
            outbound_topic: str) -> None:
        super().__init__(project_id,
                         inbound_topic,
                         outbound_topic)
        self.inbound_subscription = (f'projects/{project_id}'
                                     f'/subscriptions/sub_{self.host_id}')

        self.futures = TTLCache(maxsize=MAX_TTL_CACHE_SIZE, ttl=JOB_CACHE_TTL)
        self.streams = TTLCache(maxsize=MAX_TTL_CACHE_SIZE,
                                ttl=JOB_CACHE_TTL)

    async def initialize(self,
                         body: dict[str, Any] | None = None,
                         *,
                         session: Session | None = None,
                         timeout: int = 10,):
        logger.info('Initializing client inbound subscription')
        default_filter = f"attributes.host_id = \"{self.host_id}\""

        # TODO: Exactly Once Delivery not needed on the client.
        if body is None:
            body = {}

        if 'filter' in body:
            body['filter'] = f"({body['filter']}) AND ({default_filter})"
        else:
            body['filter'] = default_filter

        await self.subscriber.create_subscription(
            subscription=self.inbound_subscription,
            topic=self.inbound_topic,
            body=body,
            session=session,
            timeout=timeout)

    async def submit(self, data: bytes | str,
                     job_id: str = None,
                     session: Session | None = None,
                     stream: bool = False,
                     timeout: int = 10) -> str | AsyncIterator:
        if job_id is None:
            job_id = str(uuid.uuid4())

        logger.info('Submitting job %s', job_id)

        attributes: dict[str, str] = {
            'job_id': str(job_id),
            'host_id': str(self.host_id)
        }
        # Create a future to await the result
        if stream:
            async_stream = self.streams[job_id] = AsyncOrderedStream(
                timeout=timeout)
            attributes['response-type'] = 'stream'
        else:
            future = self.futures[job_id] = asyncio.Future()

        messages = [
            PubsubMessage(data, **attributes)
        ]
        # Add try except block to clean up on failure
        await self.publisher.publish(
            topic=self.outbound_topic,
            messages=messages,
            session=session,
            timeout=timeout)

        if stream:
            return async_stream
        else:
            result = await future
            return result

    async def _on_message(self, message: SubscriberMessage) -> None:
        data = (message.data or b'').decode()
        job_id = message.attributes.get('job_id')
        response_type = message.attributes.get('response-type')
        logger.info('client received job %s with message %s via %s',
                    job_id, data, response_type)

        if job_id in self.futures or job_id in self.streams:
            logging.info(message.attributes)

            if response_type == 'stream':
                job = self.streams[job_id]
                sender = message.attributes.get('sender')
                # Check for message order, otherwise, set as next message
                message_order = message.attributes.get('message_order')
                if message_order is None:
                    raise KeyError('The attribute message_order not found'
                                   ' in the streamed, the server response'
                                   ' is malformed.')
                # Check control flow, only eos supported
                logger.info('Message order %s', message_order)
                message_order = int(message_order)
                eos = message.attributes.get('eos')
                if eos == 'eos':
                    await job.signal_end_of_stream(message_order, sender)
                    # Cleanup job tracking
                    del self.streams[job_id]
                else:
                    await job.add(data, message_order, sender)
            else:
                job = self.futures[job_id]
                logger.info('Non stream job, setting future result')
                job.set_result(data)
                # Cleanup job tracking
                del self.futures[job_id]


class PubSubRPCServer(PubSubRPCBase):
    def __init__(
            self,
            project_id: str,
            inbound_subscription_name: str,
            inbound_topic: str,
            outbound_topic: str) -> None:
        super().__init__(project_id, inbound_topic, outbound_topic)
        self.inbound_subscription = (f'projects/{project_id}'
                                     f'/subscriptions/{inbound_subscription_name}')
        self.publish_queue: asyncio.Queue[PubsubMessage] = asyncio.Queue()

    async def startup(self) -> None:
        await super().startup()

        async def producer(messages: list[PubsubMessage]):
            try:
                await self.publisher.publish(self.outbound_topic,
                                             messages)
            except Exception:
                logger.exception('Network error, failed to publish')

        self.producer = asyncio.create_task(self._queue_worker(
            self.publish_queue,
            'publisher',
            PRODUCER_MAX_WAIT_TIME,
            PUBLISH_BATCH_SIZE,
            producer))

    async def initialize(self,
                         body: dict[str, Any] | None = None,
                         *,
                         session: Session | None = None,
                         timeout: int = 10,):
        logger.info('Initializing server inbound subscription')

        if body is None:
            body = {'enableExactlyOnceDelivery': True}
        else:
            body.update({'enableExactlyOnceDelivery': True})

        try:
            await self.subscriber.create_subscription(
                subscription=self.inbound_subscription,
                topic=self.inbound_topic,
                body=body,
                session=session,
                timeout=timeout)
        except Exception:
            logging.exception(
                'An error occured making a server subscription')

    async def _on_message(self, message: SubscriberMessage):
        logger.info(f'Stream server: {message}')

        response_type = message.attributes.get('response-type')
        logging.info('Response type of message is %s', response_type)
        if response_type == 'stream':
            # attributes['response-type'] = response_type

            order = 0
            async for response in self.process_stream_message(message):
                response.attributes.update(message.attributes)
                response.attributes['message_order'] = str(order)
                response.attributes['sender'] = str(self.host_id)

                logger.info(f'Queueing response {response} into producer')
                await self.publish_queue.put(response)
                order += 1

            # Send the eos signal
            eos = PubsubMessage('', eos='eos',
                                message_order=str(order),
                                sender=str(self.host_id),
                                **message.attributes)
            await self.publish_queue.put(eos)
        elif response_type is None:
            logger.info('Message received')
            responses: list[PubsubMessage] = await self.process_message(
                message)

            for response in responses:
                response.attributes.update(message.attributes)
                logger.info('Response to non-stream is %s', response)
                await self.publish_queue.put(response)
        else:
            raise ValueError('Unexpected response-type'
                             f' received: {response_type}')

    async def process_message(
            self, message: SubscriberMessage) -> list[PubsubMessage]:
        """The user-defined, per-message transform to apply to a message"""
        raise NotImplementedError

    async def process_stream_message(
            self, message: SubscriberMessage) -> AsyncIterator[PubsubMessage]:
        """The user-defined, streaming, per-message transform to apply
        to a message"""
        raise NotImplementedError
