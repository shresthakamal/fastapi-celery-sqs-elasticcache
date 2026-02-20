import os

from fastapi import FastAPI

from api import tasks_router

from config import settings
from loguru import logger



app = FastAPI(
    title="learn-rabbitmq",
    description="FastAPI + RabbitMQ + Celery learning project",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(tasks_router, prefix="/api")

logger.info(f"Settings: {settings.model_dump_json()}")


@app.get("/health")
def get_health() -> dict[str, str]:

    return {
        "environment": os.environ,
        "settings": settings.model_dump_json(),
    }   