from logging.mdc.adapter import MappedDiagnosticAdapter
from logging.mdc.no_op import NoOpMappedDiagnosticAdapter


class MappedDiagnosticContext:
    def __init__(self, adapter: MappedDiagnosticAdapter = None):
        if adapter is None:
            adapter = NoOpMappedDiagnosticAdapter()
        self.adapter: MappedDiagnosticAdapter = adapter

    def put(self, key: str, val: str) -> None:
        self.adapter.put(key, val)

    def get(self, key: str) -> str:
        return self.adapter.get(key)

    def remove(self, key: str) -> None:
        return self.adapter.remove(key)

    def clear(self) -> None:
        return self.adapter.clear()
