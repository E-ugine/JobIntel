from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.db.models import ScrapeLog
from app.api.schemas import ScrapeLogOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/logs", response_model=list[ScrapeLogOut])
def list_logs(db: Session = Depends(get_db), limit: int = 10):
    """List the most recent scrape runs."""
    return db.query(ScrapeLog).order_by(ScrapeLog.started_at.desc()).limit(limit).all()

@router.get("/stats")
def global_stats(db: Session = Depends(get_db)):
    """Aggregate overall scraping stats."""
    total_runs = db.query(func.count(ScrapeLog.id)).scalar()
    avg_duration = db.query(func.avg(ScrapeLog.duration)).scalar()
    total_created = db.query(func.sum(ScrapeLog.created)).scalar() or 0
    total_updated = db.query(func.sum(ScrapeLog.updated)).scalar() or 0
    total_skipped = db.query(func.sum(ScrapeLog.skipped)).scalar() or 0

    return {
        "total_runs": total_runs,
        "avg_duration_sec": round(avg_duration or 0, 2),
        "total_created": total_created,
        "total_updated": total_updated,
        "total_skipped": total_skipped,
    }
