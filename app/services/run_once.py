from app.services.scraper import scrape_remoteok
from app.services.ingest import upsert_jobs
from app.db.session import SessionLocal

def run_scrape_and_ingest(limit: int = 30):
    db = SessionLocal()
    try:
        data = scrape_remoteok(limit=limit)
        result = upsert_jobs(db, data)
        return result
    finally:
        db.close()

if __name__ == "__main__":
    result = run_scrape_and_ingest(30)
    print(f"Ingestion Summary → {result}")

