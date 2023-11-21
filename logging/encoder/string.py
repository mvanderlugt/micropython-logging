from logging.encoder.encoder import Encoder
from logging.levels import Levels
from logging.log_event import LogEvent


class StringEncoder(Encoder):
    def __init__(self, name: str):
        super().__init__(name)

    def encode(self, event: LogEvent) -> str:
        level = Levels.get_name(event.level)
        year, month, day, hour, minute, second = event.time
        message = event.message
        if len(event.args) > 0:
            message = event.message.format(*event.args)
        return '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}  {:>8} --- {:<40} : {}'.format(
            year, month, day,
            hour, minute, second,
            level,
            event.logger_name,  # todo abbreviate long names
            message)
