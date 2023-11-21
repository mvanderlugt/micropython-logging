from logging.appender.base import Appender
from logging.encoder.encoder import Encoder
from logging.log_event import LogEvent


class StandardOutAppender(Appender):
    def __init__(self, name: str, encoder: Encoder):
        super().__init__(name, encoder)

    def __str__(self):
        return f"StandardOutAppender('{self.name}', {self.encoder})"

    async def write(self, event: LogEvent):
        print(self.encoder.encode(event))
