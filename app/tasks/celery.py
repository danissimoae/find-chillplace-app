from celery import Celery

from app.config import CELERY_BROKER_URL

celery = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    include=["app.tasks.tasks"]
)

