JobIntel — Intelligent Job Market Insights API

JobIntel is a backend data intelligence system built with FastAPI.
It scrapes, cleans, and structures job listings into a unified, queryable dataset — helping teams visualize hiring trends, skill demand, and salary insights across the market.

Overview:
Job data today is scattered across platforms and inconsistent in structure.
JobIntel solves that by automating the entire collection-to-insight pipeline:

Scrape job listings from sources like RemoteOK.

Normalize and store them in PostgreSQL using SQLAlchemy.

Process tasks asynchronously with Celery and Redis.

Expose the data via a clean FastAPI interface and simple dashboards.

The result — a reliable, self-updating API and dashboard that turns raw job data into intelligence.


Tech Stack:
Backend: FastAPI, SQLAlchemy, Celery, Redis, Playwright
Database: PostgreSQL
Frontend (Dashboard): Jinja2 Templates, Chart.js, Tailwind CSS
Infrastructure: Docker-ready architecture for Postgres, Redis, Celery, and API services

Core Features:
Layer	Description
Automated Scraper ~ A Playwright-based engine scrapes job listings (title, company, tech stack, salary, etc.) from RemoteOK and normalizes them into structured records.
Persistent Storage ~ SQLAlchemy ORM models store the data in PostgreSQL with deduplication and timestamps to ensure freshness.
Task Scheduling	~ Celery workers (with Redis as the broker) manage scraping and data cleaning asynchronously. Celery Beat automates recurring runs.
API Endpoints ~ FastAPI provides REST endpoints for job data, insights, logs, and scrape triggers.
Dashboards ~	/dashboard monitors system health and scrape metrics; /insights visualizes top skills, job titles, salaries, and posting trends.
Automation Loop ~	/api/scrape → Celery task → Scraper → Database → Logs → Dashboard — the entire cycle runs automatically.

Local Setup
1. Clone and Install
git clone https://github.com/E-ugine/JobIntel.git
cd jobintel
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Configure Environment

Create a .env file in the root directory:

DATABASE_URL=postgresql://<user>:<password>@localhost:5432/jobintel
REDIS_URL=redis://localhost:6379/0
API_BASE=http://127.0.0.1:8000

3. Start Services

Start PostgreSQL and Redis (manually or with Docker):

redis-server
pg_ctl -D /usr/local/var/postgres start

4. Run the Application

Start Celery workers and the FastAPI server:

# Workers and scheduler
celery -A app.worker.celery worker --loglevel=info
celery -A app.worker.celery beat --loglevel=info

# API server
uvicorn app.main:app --reload

5. Trigger a Scrape
curl -X POST http://127.0.0.1:8000/api/scrape


This will enqueue a Celery task that scrapes data, stores it in PostgreSQL, and updates the dashboard automatically.

Dashboards
URL	Purpose
/dashboard	Monitor scrape runs, job counts, success rate, and durations
/insights	Visualize top skills, salaries, job titles, and posting frequency

Next Steps:
Add more job sources (LinkedIn, Indeed, WeWorkRemotely).
Deploy on Docker Compose with persistent volumes.
Extend analytics layer with ML-based skill clustering.