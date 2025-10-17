from app.services.scrapers.remoteok_scraper import scrape_remoteok
from app.services.scrapers.weworkremotely_scraper import scrape_weworkremotely
from app.services.ingest import upsert_jobs
from app.db.session import SessionLocal


def run_scrape_and_ingest(limit: int = 30):
    db = SessionLocal()
    try:
        all_jobs = []
        summary = {}

        #Scrape RemoteOK
        print("🔍 Scraping from RemoteOK...")
        remoteok_data = scrape_remoteok(limit=limit)
        summary["RemoteOK"] = len(remoteok_data)
        all_jobs.extend(remoteok_data)

        #Scrape WeWorkRemotely
        print("🔍 Scraping from WeWorkRemotely...")
        wwr_data = scrape_weworkremotely(limit=limit)
        summary["WeWorkRemotely"] = len(wwr_data)
        all_jobs.extend(wwr_data)

        #Ingest Combined Data
        print("💾 Ingesting all scraped jobs...")
        result = upsert_jobs(db, all_jobs)

        print("\n📊 Summary:")
        for source, count in summary.items():
            print(f"  - {source}: {count} jobs scraped")
        print(f"\n✅ Ingestion Summary → {result}")

        return {"sources": summary, "ingestion": result}

    finally:
        db.close()


if __name__ == "__main__":
    result = run_scrape_and_ingest(30)
    print("\n🏁 All scraping and ingestion complete.")
