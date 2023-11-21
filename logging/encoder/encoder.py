from logging.log_event import LogEvent


class Encoder:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    def encode(self, event: LogEvent) -> str:
        raise NotImplementedError
