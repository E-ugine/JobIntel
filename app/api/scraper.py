from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from app.tasks.scraper_tasks import run_remoteok_scraper

router = APIRouter(prefix="/api/scrape", tags=["Scraper"])

@router.post("/", summary="Trigger job scraping manually")
async def trigger_scrape():
    """Enqueue a scraping task via Celery."""
    task = run_remoteok_scraper.delay()
    return JSONResponse({
        "message": "Scraping started in background.",
        "task_id": task.id
    })
