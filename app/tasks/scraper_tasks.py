from datetime import datetime
from app.core.celery_app import celery
from app.services.run_once import run_scrape_and_ingest
from app.db.session import SessionLocal
from app.db.models import ScrapeLog

@celery.task(name="run_remoteok_scraper")
def run_remoteok_scraper(limit: int = 30):
    """Background scraping task with run logging."""
    db = SessionLocal()
    start_time = datetime.utcnow()
    task_id = run_remoteok_scraper.request.id
    log_entry = ScrapeLog(task_id=task_id, status="running", started_at=start_time)
    db.add(log_entry)
    db.commit()

    try:
        print(" Starting background scrape task...")
        result = run_scrape_and_ingest(limit)

        finish_time = datetime.utcnow()
        duration = (finish_time - start_time).total_seconds()

        log_entry.status = "success"
        log_entry.finished_at = finish_time
        log_entry.duration = duration
        log_entry.created = result.get("created", 0)
        log_entry.updated = result.get("updated", 0)
        log_entry.skipped = result.get("skipped", 0)
        db.commit()

        print(f"✅ Scrape complete: {result}")
        return result

    except Exception as e:
        finish_time = datetime.utcnow()
        log_entry.status = "failed"
        log_entry.finished_at = finish_time
        log_entry.duration = (finish_time - start_time).total_seconds()
        db.commit()
        print(f"❌ Scrape failed: {e}")
        raise

    finally:
        db.close()
