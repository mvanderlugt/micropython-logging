class MappedDiagnosticAdapter:
    def put(self, key: str, val: str) -> None:
        raise NotImplementedError

    def get(self, key: str) -> str:
        raise NotImplementedError

    def remove(self, key: str) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError
