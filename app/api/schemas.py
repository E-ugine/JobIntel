from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class JobBase(BaseModel):
    title: str
    company: Optional[str]
    location: Optional[str]
    salary: Optional[str]
    tech_stack: Optional[str]
    job_type: Optional[str]
    logo: Optional[str]
    source: str
    external_id: str
    apply_url: Optional[str]
    date_posted: Optional[datetime]

    class Config:
        orm_mode = True  # allows reading directly from SQLAlchemy objects


class JobListResponse(BaseModel):
    count: int
    results: list[JobBase]


class SkillTrend(BaseModel):
    skill: str
    count: int

class ScrapeLogOut(BaseModel):
    id: int
    task_id: str
    status: str
    created: int
    updated: int
    skipped: int
    started_at: datetime
    finished_at: datetime | None
    duration: float | None

    class Config:
        orm_mode = True