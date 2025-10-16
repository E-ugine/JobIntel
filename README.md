JobIntel — Intelligent Job Market Insights API

JobIntel is an intelligent backend system that automatically scrapes remote tech job listings, stores them in a structured PostgreSQL database, and exposes real-time analytics through a REST API and interactive dashboards.

Tech Stack

Backend: FastAPI · SQLAlchemy · Celery · Redis · Playwright
Database: PostgreSQL
Frontend (Dashboard): Jinja2 Templates · Chart.js · Tailwind CSS
Infrastructure: Docker-ready architecture for Postgres + Redis + Celery + API

Core Features
Layer	Description
🧠 Automated Scraper	Playwright-based engine scrapes job listings (title, company, tech stack, salary, etc.) from RemoteOK and normalizes them into structured records.
🗄️ Persistent Storage	SQLAlchemy ORM models map data into PostgreSQL with deduplication and timestamps for freshness.
⚙️ Task Scheduling	Celery workers (with Redis broker) handle asynchronous scraping tasks; Celery Beat automates recurring runs.
🌐 FastAPI Backend	RESTful endpoints for job data, insights, logs, and scrape triggers (/api/jobs, /api/insights, /api/scrape).
📊 Dashboards	/dashboard monitors system health (runs, success rate, durations); /insights visualizes market data (top skills, salaries, posting trends).
🔁 Full Automation Loop	/api/scrape → Celery task → Scraper → PostgreSQL → Logs → Dashboard updates.
🧩 API Overview
Endpoint	Method	Description
/api/scrape	POST	Triggers a background scrape job
/api/jobs	GET	Fetches stored job listings
/api/insights/summary	GET	Dataset summary (total jobs, unique companies, etc.)
/api/insights/top-skills	GET	Most in-demand technologies
/api/insights/salary-ranges	GET	Salary range distribution
/api/insights/top-titles	GET	Most common job titles
/api/insights/post-frequency	GET	Daily/weekly posting frequency
/api/logs	GET	Recent scrape run logs
/api/stats	GET	Aggregated system stats
🚀 Local Setup
1️⃣ Clone & Install
git clone https://github.com/<your-username>/jobintel.git
cd jobintel
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2️⃣ Configure Environment

Create .env:

DATABASE_URL=postgresql://<user>:<password>@localhost:5432/jobintel
REDIS_URL=redis://localhost:6379/0
API_BASE=http://127.0.0.1:8000

3️⃣ Run Services

Start PostgreSQL and Redis (locally or via Docker):

redis-server
pg_ctl -D /usr/local/var/postgres start

4️⃣ Start Workers & API
# Celery worker and scheduler
celery -A app.worker.celery worker --loglevel=info
celery -A app.worker.celery beat --loglevel=info

# FastAPI server
uvicorn app.main:app --reload

5️⃣ Trigger Scraper
curl -X POST http://127.0.0.1:8000/api/scrape


✅ This enqueues a Celery task that scrapes data and updates the database automatically.

🧾 Dashboards
URL	Purpose
/dashboard	View scraper logs, job count, average duration, success rate, and manual trigger button
/insights	Analyze market trends: top skills, job titles, salaries, sources, and posting frequency

