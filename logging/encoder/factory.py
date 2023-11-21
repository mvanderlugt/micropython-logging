from logging.encoder.encoder import Encoder
from logging.encoder.json import JsonEncoder
from logging.encoder.string import StringEncoder


class EncoderFactory:
    @classmethod
    def default_encoder(cls) -> Encoder:
        return StringEncoder("Default")

    @classmethod
    def create_encoder(cls, config: dict[str, any]) -> Encoder:
        encoder_name = config.get("name")
        encoder_class = config.get("class")
        if encoder_class == StringEncoder.__name__:
            return StringEncoder(encoder_name)
        elif encoder_class == JsonEncoder.__name__:
            return JsonEncoder(encoder_name)
        else:
            print(f"Warning: Invalid logging encoder configuration = {config}")
            return StringEncoder("Default")
