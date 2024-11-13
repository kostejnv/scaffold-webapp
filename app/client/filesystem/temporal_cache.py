from aiocache import Cache
from beacon.client.filesystem.file_manager import FileManager


class TemporalCache(FileManager):
    def __init__(self, cache: Cache):
        self.cache = cache

    async def read(self, path: str) -> object:
        return await self.cache.get(path)

    async def write(self, path: str, content: object) -> None:
        await self.cache.set(path, content)
