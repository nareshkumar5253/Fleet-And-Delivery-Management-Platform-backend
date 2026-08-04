import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://fleet_redis:6379/0"
)

celery = Celery(
    "fleet_management",
    broker=REDIS_URL,
    backend=REDIS_URL
)


celery.conf.update(
    task_track_started=True,
    timezone="UTC",
)


# IMPORTANT
celery.autodiscover_tasks(
    [
        "app.tasks",
        "app.worker"
    ]
)