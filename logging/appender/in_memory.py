from collections import deque

from logging.appender.base import Appender
from logging.encoder.encoder import Encoder
from logging.log_event import LogEvent


class InMemoryAppender(Appender):
    def __init__(self, name: str, encoder: Encoder, max_messages: int = 25):
        super().__init__(name, encoder)
        self.max_messages = max_messages
        self.messages = deque((), max_messages)

    def __str__(self):
        return f"InMemoryAppender('{self.name}', {self.encoder}, {self.max_messages})"

    async def write(self, event: LogEvent):
        self.messages.append(self.encoder.encode(event))
