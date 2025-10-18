from celery import Celery
from celery.schedules import crontab
import os

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery(
    "jobintel",
    broker=redis_url,
    backend=redis_url,
    include=["app.tasks.scraper_tasks"],
)

celery.conf.update(
    result_expires=3600,
    timezone="UTC",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],

    beat_scheduler="redbeat.RedBeatScheduler",
    redbeat_redis_url=redis_url,
)

celery.conf.beat_schedule = {
    "run-remoteok-hourly": {
        "task": "run_remoteok_scraper",
        "schedule": crontab(minute=0, hour="*/1"),
        "args": (30,),
    },
}
