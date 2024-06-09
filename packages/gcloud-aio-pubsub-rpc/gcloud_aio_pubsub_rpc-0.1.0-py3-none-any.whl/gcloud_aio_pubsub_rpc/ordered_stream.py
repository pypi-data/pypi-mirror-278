import asyncio
from typing import Any

import logging

logger = logging.getLogger(__name__)


class AsyncOrderedStream:
    def __init__(self, timeout: int = 10) -> None:
        self._queue: asyncio.Queue() = asyncio.Queue()
        self._storage: dict = {}
        self._expected_order: int = 0
        self._timeout: int = timeout
        self._sender: str | None = None

    async def add(self, item: Any, order: int, sender: str) -> None:
        """Adds an item with its order to the generator storage."""
        logging.info('%s, Got %s, waiting for %s, %s, %s', item, order, self._expected_order, sender, self._storage)
        if self._sender is None:
            # This is the first packet received, expect future packets
            # to come from this sender
            logging.info('Setting sender to %s', sender)
            self._sender = sender
        elif self._sender != sender:
            # This packet is from a different sender, ignore it
            # logger.error('Got a message from %s, expectinf from %s', sender, self._sender)
            raise Exception(
                'Got a message from %s, expecting %s', sender, self._sender)

        if order == self._expected_order:
            await self._queue.put(item)
            self._expected_order += 1
            # Check if the next items are already in storage
            while self._expected_order in self._storage:
                logging.info('Popping %s from storage', self._storage[self._expected_order])
                await self._queue.put(self._storage.pop(self._expected_order))
                self._expected_order += 1
        elif order < self._expected_order:
            # Message has already been recieved
            logging.info('Got an earlier message, past that')
            pass
        else:
            logging.info('Storing %s in storage at order %s', item, order)
            self._storage[order] = item

    async def signal_end_of_stream(self, total_iterables: int, sender: str):
        await self.add(StopAsyncIteration, total_iterables, sender)

    def __aiter__(self) -> 'AsyncOrderedStream':
        """Makes this object an asynchronous iterator."""
        return self

    # TODO: The following wait_for is not cancelled and delays
    #       shutdown on signal interuptions
    async def __anext__(self) -> Any:
        """Wait for the next item from the generator."""
        # if self._completed:
        #     raise StopAsyncIteration
        item = await asyncio.wait_for(self._queue.get(), self._timeout)
        if item is StopAsyncIteration:
            raise item
        return item
