from celery.result import AsyncResult
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.celery import app as celery_app
from tasks.add import add

router = APIRouter(prefix="/tasks", tags=["tasks"])

class AddTaskRequest(BaseModel):
    a: int = Field(..., description="First number")
    b: int = Field(..., description="Second number")


@router.post("/add")
def create_add_task(payload: AddTaskRequest) -> dict[str, str]:
    async_result = add.delay(payload.a, payload.b)
    return {
        "task_id": async_result.id,
        "status": "queued",
    }


@router.get("/{task_id}")
def get_task_status(task_id: str) -> dict[str, str | int | None]:
    result = AsyncResult(task_id, app=celery_app)
    response: dict[str, str | int | None] = {
        "task_id": task_id,
        "status": result.status,
    }
    if result.ready():
        response["result"] = result.result
    return response
