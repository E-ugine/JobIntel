from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import SessionLocal
from app.db.models import Job
from app.api.schemas import JobListResponse, JobBase

router = APIRouter()

# Dependency: DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/jobs", response_model=JobListResponse)
def list_jobs(
    db: Session = Depends(get_db),
    source: str | None = Query(None),
    company: str | None = Query(None),
    tech: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """List and filter jobs with pagination."""
    query = select(Job)

    if source:
        query = query.where(Job.source.ilike(f"%{source}%"))
    if company:
        query = query.where(Job.company.ilike(f"%{company}%"))
    if tech:
        query = query.where(Job.tech_stack.ilike(f"%{tech}%"))

    total = db.query(Job).count()
    jobs = db.execute(query.offset(offset).limit(limit)).scalars().all()

    return {"count": total, "results": jobs}
