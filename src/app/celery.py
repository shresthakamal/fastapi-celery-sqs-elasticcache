from celery import Celery
from kombu.utils.url import safequote
from config import settings


aws_access_key = safequote(settings.AWS_ACCESS_KEY_ID)
aws_secret_key = safequote(settings.AWS_SECRET_ACCESS_KEY)

broker_url = "sqs://{aws_access_key}:{aws_secret_key}@".format(
    aws_access_key=aws_access_key, aws_secret_key=aws_secret_key,
)

result_backend = settings.CELERY_RESULT_BACKEND


app = Celery(
    "app",
    broker=broker_url,
    backend=result_backend,
    include=["tasks"],
)

transport_options = {
    "region": settings.AWS_REGION,
    "visibility_timeout": 3600,
    "predefined_queues": {
        settings.SQS_QUEUE_NAME: {
            "url": settings.SQS_QUEUE_URL,
            "access_key_id": settings.AWS_ACCESS_KEY_ID,
            "secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
        }
    },
}

if settings.AWS_ENDPOINT_URL:
    transport_options["endpoint_url"] = settings.AWS_ENDPOINT_URL

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