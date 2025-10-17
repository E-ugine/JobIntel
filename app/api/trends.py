from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal
from app.api.schemas import SkillTrend

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/trends/skills", response_model=list[SkillTrend])
def top_skills(db: Session = Depends(get_db), limit: int = 10):
    """
    Aggregate top skills from the tech_stack field.
    """
    sql = text("""
        SELECT skill, COUNT(*) AS count FROM (
            SELECT LOWER(TRIM(unnest(string_to_array(tech_stack, ',')))) AS skill
            FROM jobs
            WHERE tech_stack IS NOT NULL AND tech_stack <> ''
        ) AS extracted
        WHERE skill NOT IN ('full time', 'remote', 'contract', 'n/a')
        AND LENGTH(skill) > 1
        GROUP BY skill
        ORDER BY count DESC
        LIMIT :limit;
    """)
    result = db.execute(sql, {"limit": limit})
    return [{"skill": row.skill, "count": row.count} for row in result]
