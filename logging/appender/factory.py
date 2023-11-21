from logging.appender.base import Appender
from logging.appender.file import FileAppender
from logging.appender.in_memory import InMemoryAppender
from logging.appender.mqtt import MqttAppender
from logging.appender.standard_out import StandardOutAppender
from logging.encoder.encoder import Encoder


class AppenderFactory:
    @classmethod
    def default_appender(cls) -> Appender:
        raise NotImplementedError

    @classmethod
    def create_appender(cls, name: str, config: dict[str, any], encoder: Encoder) -> Appender:
        appender_class = config["class"]
        if appender_class == InMemoryAppender.__name__:
            return AppenderFactory.create_in_memory_appender(name, config, encoder)
        elif appender_class == StandardOutAppender.__name__:
            return StandardOutAppender(name, encoder)
        elif appender_class == MqttAppender.__name__:
            return AppenderFactory.create_mqtt_appender(name, config, encoder)
        elif appender_class == FileAppender.__name__:
            return AppenderFactory.create_file_appender(name, config, encoder)
        else:
            print(f"Warning: Invalid appender configuration, class {appender_class} not supported")

    @classmethod
    def create_in_memory_appender(cls, name, config, encoder):
        if "max_messages" in config:
            max_messages = config["max_messages"]
            return InMemoryAppender(name, encoder, max_messages)
        else:
            return InMemoryAppender(name, encoder)

    @classmethod
    def create_mqtt_appender(cls, name, config, encoder):
        from mqtt.client import MQTT

        if "client_id" in config and "host" in config and "port" in config:
            mqtt = MQTT(config["client_id"], config["host"], config["port"],
                        config.get("username"), config.get("password"))
            if "topic" in config:
                return MqttAppender(name, encoder, mqtt, config["topic"])
            else:
                return MqttAppender(name, encoder, mqtt)
        else:
            print(f"Warning: Invalid appender configuration, cannot connect to MQTT = {config}")

    @classmethod
    def create_file_appender(cls, name, config, encoder):
        if "file_path" in config:
            return FileAppender(name, encoder, config["file_path"])
        else:
            return FileAppender(name, encoder)
