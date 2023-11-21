from logging.mdc.adapter import MappedDiagnosticAdapter


class BasicMappedDiagnosticAdapter(MappedDiagnosticAdapter):
    def __init__(self):
        self.fields: dict = dict()

    def put(self, key: str, val: str) -> None:
        self.fields[key] = val

    def get(self, key: str) -> str:
        return self.fields[key]

    def remove(self, key: str) -> None:
        _ = self.fields.pop(key)

    def clear(self) -> None:
        self.fields.clear()
