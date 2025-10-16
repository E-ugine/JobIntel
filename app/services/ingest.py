from typing import Iterable, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import Job

UPSERT_FIELDS = [
    "title", "company", "location", "tech_stack", "job_type", "salary",
    "logo", "apply_url", "date_posted"
]

def _apply_updates(job: Job, data: Dict[str, Any]) -> bool:
    """Update fields if changed. Returns True if any field changed."""
    changed = False
    for f in UPSERT_FIELDS:
        new_val = data.get(f)
        if getattr(job, f) != new_val:
            setattr(job, f, new_val)
            changed = True
    return changed

def upsert_jobs(db: Session, jobs: Iterable[Dict[str, Any]]) -> dict:
    """
    Idempotent upsert:
    - Insert new jobs
    - Update existing ones only if data changed
    Returns: {"created": X, "updated": Y, "skipped": Z}
    """
    created = updated = skipped = 0

    for payload in jobs:
        source = payload.get("source")
        external_id = payload.get("external_id")
        if not source or not external_id:
            skipped += 1
            continue

        # Find existing
        existing = db.execute(
            select(Job).where(Job.source == source, Job.external_id == external_id)
        ).scalar_one_or_none()

        if existing:
            if _apply_updates(existing, payload):
                updated += 1
            else:
                skipped += 1
        else:
            rec = Job(**payload)
            db.add(rec)
            created += 1

    db.commit()
    return {"created": created, "updated": updated, "skipped": skipped}
