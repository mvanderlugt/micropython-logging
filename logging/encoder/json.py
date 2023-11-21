from json import dumps

from logging.encoder.encoder import Encoder
from logging.levels import Levels
from logging.log_event import LogEvent


class JsonEncoder(Encoder):
    def __init__(self, name: str):
        super().__init__(name)

    def encode(self, event: LogEvent) -> str:
        level = Levels.get_name(event.level)
        year, month, day, hour, minute, second = event.time
        time = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(year, month, day, hour, minute, second)
        message = event.message
        if len(event.args) > 0:
            message = event.message.format(*event.args)
        return dumps(dict(time=time, level=level, logger=event.logger_name, message=message))
