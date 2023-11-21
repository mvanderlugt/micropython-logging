from logging.appender.base import Appender
from logging.encoder.encoder import Encoder
from logging.log_event import LogEvent
from mqtt.client import MQTT


class MqttAppender(Appender):
    def __init__(self, name: str, encoder: Encoder, mqtt: MQTT, topic: str = 'log'):
        super().__init__(name, encoder)
        self.mqtt = mqtt
        self.topic = topic

    async def start(self):
        await self.mqtt.connect()
        await super().start()

    async def write(self, event: LogEvent):
        # todo logging that I logged logs to mqtt
        if not event.logger_name.startswith('mqtt'):
            await self.mqtt.publish(self.topic, self.encoder.encode(event))
