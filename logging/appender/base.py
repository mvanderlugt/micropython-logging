from asyncio import sleep, CancelledError
from collections import deque

from logging.encoder.encoder import Encoder
from logging.log_event import LogEvent


class Appender:
    def __init__(self, name: str, encoder: Encoder = None, max_queue_size: int = 10):
        self.name: str = name
        self.encoder: Encoder | None = encoder
        self._messages: deque = deque((), max_queue_size)
        self._running = False

    def append(self, event: LogEvent) -> None:
        self._messages.append(event)

    async def write(self, event: LogEvent):
        raise NotImplementedError

    async def start(self):
        self._running = True
        while self._running:
            try:
                if len(self._messages) > 0:
                    message = self._messages.popleft()
                    await self.write(message)
            except CancelledError:
                print(f"Logging writer {self.name} cancelled")
            except Exception as error:
                print("Uncaught exception: {}", str(error))
            finally:
                await sleep(0)
