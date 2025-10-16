from celery import Celery
from celery.schedules import crontab
import os

# ─────────────────────────────────────────────
# Redis configuration
# ─────────────────────────────────────────────
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "jobintel",
    broker=redis_url,
    backend=redis_url,
    include=["app.tasks.scraper_tasks"],
)

# ─────────────────────────────────────────────
# Core Celery configuration
# ─────────────────────────────────────────────
celery.conf.update(
    result_expires=3600,             # Task result TTL
    timezone="UTC",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)

# ─────────────────────────────────────────────
# Periodic tasks (Celery Beat schedule)
# ─────────────────────────────────────────────
celery.conf.beat_schedule = {
    # Every 6 hours: run scraper with limit 30
    "run-scraper-every-6-hours": {
        "task": "run_remoteok_scraper",
        "schedule": crontab(minute=0, hour="*/1"),
        "args": (30,),
    },
    # Optional: once a day at midnight
    # "daily-refresh": {
    #     "task": "run_remoteok_scraper",
    #     "schedule": crontab(minute=0, hour=0),
    #     "args": (50,),
    # },
}
