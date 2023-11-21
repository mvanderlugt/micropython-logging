from logging.logger import Logger
from logging.logging_context import LoggingContext


def get_logger(name: str) -> Logger:
    return LoggingContext().get_logger(name)
