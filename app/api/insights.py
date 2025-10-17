from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.db.session import get_db
from app.db.models import Job

router = APIRouter(prefix="/api/insights", tags=["Insights"])

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total_jobs = db.query(func.count(Job.id)).scalar()
    unique_companies = db.query(func.count(func.distinct(Job.company))).scalar()
    unique_skills = db.query(func.count(func.distinct(Job.tech_stack))).scalar()
    last_update = db.query(func.max(Job.date_posted)).scalar()

    return {
        "total_jobs": total_jobs or 0,
        "unique_companies": unique_companies or 0,
        "unique_skills": unique_skills or 0,
        "last_update": last_update or None,
    }


##Top 10 In-Demand Skills
@router.get("/top-skills")
def top_skills(db: Session = Depends(get_db)):
    all_stacks = db.query(Job.tech_stack).filter(Job.tech_stack.isnot(None)).all()
    freq = {}
    for (stack,) in all_stacks:
        for skill in stack.split(","):
            s = skill.strip().lower()
            if not s:
                continue
            freq[s] = freq.get(s, 0) + 1

    sorted_skills = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
    return [{"skill": s, "count": c} for s, c in sorted_skills]


##Most Common Job Titles
@router.get("/top-titles")
def top_titles(db: Session = Depends(get_db)):
    titles = (
        db.query(Job.title, func.count(Job.title))
        .group_by(Job.title)
        .order_by(func.count(Job.title).desc())
        .limit(10)
        .all()
    )
    return [{"title": t, "count": c} for t, c in titles]


## Salary Range Breakdown
@router.get("/salary-ranges")
def salary_ranges(db: Session = Depends(get_db)):
    all_salaries = db.query(Job.salary).filter(Job.salary.isnot(None)).all()
    ranges = {
        "0-49k": 0,
        "50-99k": 0,
        "100-149k": 0,
        "150k+": 0,
    }
    for (s,) in all_salaries:
        if not s:
            continue
        digits = "".join(ch for ch in s if ch.isdigit())
        if not digits:
            continue
        val = int(digits)
        if val < 50:
            ranges["0-49k"] += 1
        elif val < 100:
            ranges["50-99k"] += 1
        elif val < 150:
            ranges["100-149k"] += 1
        else:
            ranges["150k+"] += 1

    return [{"range": r, "count": c} for r, c in ranges.items()]


## Remote Job Distribution by Source
@router.get("/job-sources")
def job_sources(db: Session = Depends(get_db)):
    sources = (
        db.query(Job.source, func.count(Job.id))
        .group_by(Job.source)
        .order_by(func.count(Job.id).desc())
        .all()
    )
    return [{"source": s, "count": c} for s, c in sources]


## Posting Frequency Over Time
@router.get("/post-frequency")
def post_frequency(db: Session = Depends(get_db)):
    cutoff = datetime.now() - timedelta(days=30)
    data = (
        db.query(func.date(Job.date_posted), func.count(Job.id))
        .filter(Job.date_posted >= cutoff)
        .group_by(func.date(Job.date_posted))
        .order_by(func.date(Job.date_posted))
        .all()
    )
    return [{"date": str(d), "count": c} for d, c in data]
