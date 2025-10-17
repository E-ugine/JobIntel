from sqlalchemy import (
    Column, Integer, String, Float, DateTime, func, UniqueConstraint, Index, Text
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False, index=True)     ## e.g "RemoteOK"
    external_id = Column(String(512), nullable=False, index=True)
    title = Column(String(300), nullable=False, index=True)
    company = Column(String(200), index=True)
    location = Column(String(120), index=True)
    tech_stack = Column(Text)
    job_type = Column(String(60))
    salary = Column(String(60))
    logo = Column(String(512))
    apply_url = Column(String(512))
    date_posted = Column(DateTime) 
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_source_external"),
        Index("ix_jobs_title_company", "title", "company"),
    )

class ScrapeLog(Base):
    __tablename__ = "scrape_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(120), index=True)
    status = Column(String(50))
    created = Column(Integer, default=0)
    updated = Column(Integer, default=0)
    skipped = Column(Integer, default=0)
    started_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime)
    duration = Column(Float)    
