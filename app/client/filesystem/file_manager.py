from typing import Protocol


class FileManager(Protocol):
    async def read(self, path: str) -> bytes:
        pass

    async def write(self, path: str, content: bytes) -> None:
        pass
