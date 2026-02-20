from celery import Celery
from config import settings


broker_url = "sqs://"

result_backend = settings.CELERY_RESULT_BACKEND


app = Celery(
    "app",
    broker=broker_url,
    backend=result_backend,
    include=["tasks"],
)

transport_options = {
    "visibility_timeout": 3600,
    "region": settings.AWS_REGION or "us-east-1",
    "queue_name_prefix": settings.SQS_QUEUE_NAME
}

app.conf.broker_transport_options = transport_options

app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,
    task_default_queue=settings.SQS_QUEUE_NAME,
)

if __name__ == "__main__":
    app.start()