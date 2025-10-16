from app.db.session import SessionLocal
from app.db.models import Job

db = SessionLocal()

for job in db.query(Job).all():
    if job.tech_stack:
        job.tech_stack = job.tech_stack.replace("  ", " ").replace("/", ",")
db.commit()
db.close()

print("✅ Tech stacks normalized successfully.")
