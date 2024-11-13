import asyncio
from functools import wraps
from http import HTTPStatus
from io import BytesIO
from logging import Logger, getLogger

import aiohttp
from aiocache import Cache, cached
from beacon.client.filesystem.file_manager import FileManager
from beacon.settings import Settings
from miniopy_async import Minio


class S3Client(FileManager):
    def __init__(self, bucket: str, settings: Settings | None = None, logger: Logger | None = None):
        self.logger = logger or getLogger(__name__)
        settings = settings or Settings()
        self.__client = Minio(
            endpoint=settings.S3_ENDPOINT_URL,
            access_key=settings.S3_ACCESS_KEY_ID,
            secret_key=settings.S3_SECRET_ACCESS_KEY,
            region=settings.S3_DEFAULT_REGION,
            secure=True,
        )
        self._bucket = bucket
        self.logger.debug("Initialized S3 client with bucket %s.", bucket)
        self.semaphore = asyncio.Semaphore(5)

    def _check_exist_bucket(func: callable) -> callable:
        """Decorator to check if the bucket exists before executing the function."""
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if not await self.__client.bucket_exists(bucket_name=self._bucket):
                error_message = f"S3 bucket {self._bucket} doesn't exists."
                self.logger.error(error_message)
                raise ValueError(error_message)
            return await func(self, *args, **kwargs)
        return wrapper

    @cached(ttl=300, cache=Cache.MEMORY)
    @_check_exist_bucket
    async def read(self, path: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with self.semaphore:
                response = await self.__client.get_object(bucket_name=self._bucket, object_name=path, session=session)
            if response.status != HTTPStatus.OK:
                error_message = f"Got status code {response.status} from S3."
                self.logger.error(error_message)
                raise ValueError(error_message)
            self.logger.debug("Read file %s from S3.", path)
            file = await response.read()
            response.close()
            return file

    @_check_exist_bucket
    async def write(self, path: str, content: bytes) -> None:
        async with self.semaphore:
            await self.__client.put_object(
                bucket_name=self._bucket,
                object_name=path,
                data=BytesIO(content),
                length=len(content),
            )
        self.logger.debug("Wrote file %s to S3.", path)
