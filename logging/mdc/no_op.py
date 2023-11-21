from logging.mdc.adapter import MappedDiagnosticAdapter


class NoOpMappedDiagnosticAdapter(MappedDiagnosticAdapter):
    def put(self, key: str, val: str) -> None:
        pass

    def get(self, key: str) -> str:
        pass

    def remove(self, key: str) -> None:
        pass

    def clear(self) -> None:
        pass
