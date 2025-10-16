from fastapi import APIRouter
from app.tasks.scraper_tasks import run_remoteok_scraper

router = APIRouter()

@router.post("/scrape/trigger")
def trigger_scrape(limit: int = 30):
    """
    Kick off a background scraping job via Celery.
    """
    task = run_remoteok_scraper.delay(limit)
    return {"message": "Scrape task queued", "task_id": task.id}
