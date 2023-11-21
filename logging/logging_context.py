from logging.appender.base import Appender
from logging.appender.standard_out import StandardOutAppender
from logging.encoder.encoder import Encoder
from logging.encoder.string import StringEncoder
from logging.levels import Levels
from logging.logger import Logger

ROOT_LOGGER_NAME = "root"
LOGGER_NAME_SEPARATOR = "."


class LoggingContext:
    __instance: 'LoggingContext' = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(LoggingContext, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # todo why is my singleton screwed up???
            self.initialized: bool = False
        if not hasattr(self, 'appenders'):
            self.appenders: dict[str, Appender] | None = dict()
        if not hasattr(self, 'root_logger'):
            self.root_logger: Logger | None = None
        if not hasattr(self, 'logger_cache'):
            self.logger_cache: dict[str, Logger] | None = dict()

    def initialize(self, config: dict) -> None:
        if not self.initialized:
            self.initialized = True
            try:
                self.__configure_appenders(config)
                self.__configure_root_logger(config)
                self.__configure_loggers(config)
            except Exception as error:
                print(f"Error: Unable to initialize logging system, error = {str(error)}")
                from sys import print_exception
                print_exception(error)
                self.initialized = False
                self.root_logger = None
                self.appenders = dict()
                self.logger_cache = dict()
        else:
            print("Warning: LoggingContext does not support re-initialization")

    def initialize_defaults(self) -> None:
        if not self.initialized:
            self.initialized = True
            self.logger_cache = dict()
            self.root_logger = Logger(ROOT_LOGGER_NAME)
            self.root_logger.level = Levels.INFO
            root_appender = StandardOutAppender("DefaultAppender", StringEncoder("DefaultEncoder"))
            self.root_logger.add_appender(root_appender)
        else:
            print("Warning: LoggingContext does not support re-initialization")

    def get_logger(self, name: str) -> Logger:
        if name == ROOT_LOGGER_NAME:
            return self.get_root_logger()

        logger = self.logger_cache.get(name)
        if not logger:
            logger = self.get_root_logger()
            parts = name.split(LOGGER_NAME_SEPARATOR)
            child_name = None
            for part in parts:
                if child_name is None:
                    child_name = part
                else:
                    child_name = f"{child_name}.{part}"
                child = self.logger_cache.get(child_name)
                if child is None:
                    child = logger.create_child(child_name)
                    self.logger_cache[child_name] = child
                logger = child
        return logger

    def get_root_logger(self) -> Logger:
        return self.root_logger

    def __configure_appenders(self, config: dict) -> None:
        self.appenders = dict()
        if "appenders" in config:
            for name, appender_config in config["appenders"].items():
                self.__configure_appender(name, appender_config)

    def __configure_root_logger(self, config: dict):
        if "root" in config:
            self.root_logger = Logger(ROOT_LOGGER_NAME)
            root_config = config["root"]
            if "level" in root_config:
                root_level = Levels.get_level(root_config["level"])
                if root_level is None:
                    raise ValueError(f"{root_config['level']} is not a valid logging level")
                self.root_logger.level = root_level
            if "appenders" in root_config:
                for appender_name in root_config["appenders"]:
                    appender = self.appenders.get(appender_name)
                    if appender is not None:
                        self.root_logger.add_appender(appender)
                    else:
                        print(f"Warning: Invalid root logger configuration, appender {appender_name} not found")
        else:
            self.root_logger = Logger(ROOT_LOGGER_NAME)
            self.root_logger.level = Levels.INFO
            self.root_logger.add_appender(StandardOutAppender("DefaultAppender", StringEncoder("DefaultEncoder")))

    def __configure_loggers(self, config: dict) -> None:
        if "loggers" in config:
            for logger_name, logger_config in config["loggers"].items():
                logger = self.get_logger(logger_name)
                if "level" in logger_config:
                    level_name = logger_config["level"]
                    level = Levels.get_level(level_name)
                    if level is not None:
                        logger.level = level
                    else:
                        print(f"Warning: Invalid logger configuration, level {level_name} not found")
                if "additive" in logger_config:
                    additive = logger_config["additive"].lower() == "true"
                    logger.additive = additive
                if "appenders" in logger_config:
                    for appender_name in logger_config["appenders"]:
                        appender = self.appenders.get(appender_name)
                        if appender is not None:
                            logger.add_appender(appender)
                        else:
                            print(f"Warning: Invalid logger configuration, appender {appender_name} not found")

    def __configure_appender(self, name: str, appender_config: dict) -> None:
        from logging.appender.factory import AppenderFactory

        encoder = LoggingContext.__get_encoder(appender_config)
        appender = AppenderFactory.create_appender(name, appender_config, encoder)
        if appender is not None:
            self.appenders[name] = appender

    @staticmethod
    def __get_encoder(appender_config: dict) -> Encoder:
        from logging.encoder.factory import EncoderFactory
        if "encoder" in appender_config:
            return EncoderFactory.create_encoder(appender_config["encoder"])
        else:
            return EncoderFactory.default_encoder()
