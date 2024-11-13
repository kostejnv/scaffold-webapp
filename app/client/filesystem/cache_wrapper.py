from aiocache import Cache
from beacon.client.filesystem.file_manager import FileManager
from beacon.settings import Settings


class CacheWrapper(FileManager):
    def __init__(self, storage: FileManager, cache: Cache, settings: Settings | None = None):
        self.storage = storage
        self.settings = settings or Settings()
        self.cache = cache

    async def read(self, path: str) -> bytes:
        if await self.cache.exists(path):
            return await self.cache.get(path)
        content = await self.storage.read(path)
        await self.cache.set(path, content)
        return content

    async def write(self, path: str, content: bytes) -> None:
        await self.storage.write(path, content)
        await self.cache.set(path, content)
