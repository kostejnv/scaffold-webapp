import asyncio
import logging

from celery import Celery

from app.settings import Settings

settings = Settings() # type: ignore

# Initialize the Celery app
celery_app = Celery(__name__,
    broker=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    backend=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
)
celery_app.conf.update(enable_utc=True, timezone="Europe/Prague")
celery_app.conf.update( # tasks can accept all python types arguments
    task_serializer="pickle",
    result_serializer="pickle",
    accept_content=["pickle"],
)

logger = logging.getLogger(__name__)

@celery_app.task(name="build_new_guide")
def test() -> str:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_test())
    loop.close()
    return result

async def async_test() -> str:
    """Async function for test purpose"""
    logger.info("Starting async test")
    await asyncio.sleep(5)
    logger.info("Finished async test")
    return "Delicate Arch"
