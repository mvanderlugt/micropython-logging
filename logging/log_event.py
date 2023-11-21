class LogEvent:
    def __init__(self, logger_name: str, level: int, time: tuple[int, int, int, int, int, int], message: str,
                 args: [any, ...]):
        self.logger_name: str = logger_name
        self.level: int = level
        self.time: tuple = time
        self.message: str = message
        self.args: [any, ...] = args
