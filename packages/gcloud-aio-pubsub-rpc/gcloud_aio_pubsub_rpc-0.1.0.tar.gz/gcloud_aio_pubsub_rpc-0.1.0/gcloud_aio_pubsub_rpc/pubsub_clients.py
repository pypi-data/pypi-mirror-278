import logging
from typing import Any
from typing import Optional

import aiohttp
import backoff
from aiohttp import ClientSession as Session
from gcloud.aio.pubsub import PublisherClient
from gcloud.aio.pubsub import PubsubMessage
from gcloud.aio.pubsub import SubscriberClient
from gcloud.aio.pubsub import SubscriberMessage

logger = logging.getLogger(__name__)


def is_http_400_error(exc: Exception):
    """Determine whether the exception is a HTTP 400 error."""
    return (isinstance(exc, aiohttp.ClientResponseError) and exc.status == 400)


def backoff_handler(details):
    logger.info(f"Backing off {details['wait']:0.1f} seconds after"
                f" {details['tries']} tries calling function"
                f" {details['target'].__name__} with args"
                f" {details['args']} and kwargs"
                 f" {details['kwargs']}")


retry = backoff.on_exception(
    backoff.expo,
    aiohttp.ClientError,
    max_time=300,  # Maximum total time in seconds
    on_backoff=backoff_handler,  # Log backoff attempts
    jitter=backoff.random_jitter,
    giveup=is_http_400_error
)


class RetryingSubscriberClient(SubscriberClient):
    @retry
    async def pull(
            self, subscription: str, max_messages: int,
            *, session: Session | None = None,
            timeout: int = 30) -> list[SubscriberMessage]:
        logger.info(f'Pulling from {subscription}')
        return await super().pull(subscription,
                                  max_messages,
                                  session=session,
                                  timeout=timeout)

    @retry
    async def acknowledge(
            self, subscription: str, ack_ids: list[str],
            *, session: Session | None = None,
            timeout: int = 10) -> None:
        logger.info(f'Acking {subscription} of {ack_ids}')
        return await super().acknowledge(subscription,
                                         ack_ids,
                                         session=session,
                                         timeout=timeout)

    @retry
    async def modify_ack_deadline(
            self, subscription: str,
            ack_ids: list[str],
            ack_deadline_seconds: int,
            *, session: Session | None = None,
            timeout: int = 10) -> None:
        logger.info(f'Modifying ack deadlines of {subscription} for {ack_ids}')
        return await super().modify_ack_deadline(subscription,
                                                 ack_ids,
                                                 ack_deadline_seconds,
                                                 session=session,
                                                 timeout=timeout)


class RetryingPublisherClient(PublisherClient):
    @retry
    async def publish(self, topic: str, messages: list[PubsubMessage],
                      session: Session | None = None,
                      timeout: int = 10) -> dict[str, Any]:
        logging.info(f'Publishing to {topic} with {messages}')
        return await super().publish(topic, messages, session, timeout)
