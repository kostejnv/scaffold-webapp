import logging

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.api.authorization import authorize
from app.api.payloads import TestPayload
from app.settings import Settings
from app.worker import test

router = APIRouter(
    prefix="/api",
)
settings = Settings() # type: ignore

logger = logging.getLogger(__name__)

@router.post("/test-task")
async def test_task(payload: TestPayload) -> JSONResponse:
    try:
        authorize(payload.authorize_token)
        logger.info("Starting to run the test task")
        task = test.delay()
        return JSONResponse(content={"task_id": task.id, "message": "Test task started."})
    except Exception as e:
        msg = f"Failed to start the test task: {e!s}"
        logger.error(msg)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": msg})

@router.get("/task/result/{task_id}")
async def task_result(task_id: str) -> JSONResponse:
    try:
        logger.info("Getting the result of the task with id: %s", task_id)
        task = test.AsyncResult(task_id)
        return JSONResponse(content={"status": task.status, "result": task.result})
    except Exception as e:
        msg = f"Failed to get the result of the task: {e!s}"
        logger.error(msg)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": msg})
