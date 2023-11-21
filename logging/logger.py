try:
    from time import gmtime
except ImportError:
    from time import localtime

    def gmtime():
        return localtime()

from asyncio import create_task

from logging.appender.base import Appender
from logging.levels import Levels
from logging.log_event import LogEvent


class Logger:
    def __init__(self, name: str,
                 parent: 'Logger' = None,
                 level: int = None,
                 additive: bool = True,
                 appenders: tuple[Appender, ...] = ()):
        self.name = name
        self.parent = parent
        self._level = level
        self.additive = additive
        self.appenders = appenders
        self.children = list()
        self.effective_level = None

    def __str__(self):
        return f"{self.__class__.__name__}('{self.name}', level=Levels.{Levels.get_name(self.level)})"

    def trace(self, message: str, *args):
        self.log(Levels.TRACE, message, *args)

    def debug(self, message: str, *args):
        self.log(Levels.DEBUG, message, *args)

    def info(self, message: str, *args):
        self.log(Levels.INFO, message, *args)

    def warning(self, message: str, *args):
        self.log(Levels.WARNING, message, *args)

    def error(self, message: str, *args):
        self.log(Levels.ERROR, message, *args)

    def log(self, level: int, message: str, *args):
        if self.__get_effective_level() <= level:
            year, month, day, hour, minute, second, _, _ = gmtime()
            event = LogEvent(self.name, level, (year, month, day, hour, minute, second), message, args)
            self.call_appenders(event)

    def call_appenders(self, event: LogEvent) -> None:
        logger = self
        while logger is not None and logger.additive:
            for appender in logger.appenders:
                appender.append(event)
            logger = logger.parent

    def add_appender(self, appender: Appender) -> None:
        self.appenders = self.appenders + (appender,)
        _ = create_task(appender.start())  # todo stop appender???

    def create_child(self, name: str) -> 'Logger':
        child = Logger(name, self)
        self.children.append(child)
        child.__handle_parent_level_change(self.__get_effective_level())
        return child

    @property
    def level(self) -> int:
        return self.effective_level

    @level.setter
    def level(self, level: int) -> None:
        self._level = level
        self.__update_effective_level()

    def __update_effective_level(self):
        if self._level is not None:
            self.effective_level = self._level
        else:
            self.effective_level = self.parent.__get_effective_level()

        for child in self.children:
            child.__handle_parent_level_change(self.__get_effective_level())

    def __get_effective_level(self) -> int:
        if self.effective_level is None and self.parent is not None:
            self.effective_level = self.parent.__get_effective_level()
        return self.effective_level

    def __handle_parent_level_change(self, level: int):
        if self._level is None:
            self.effective_level = level
            for child in self.children:
                child.__handle_parent_level_change(level)
