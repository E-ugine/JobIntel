<a name="readme-top"></a>

<div align="center"> <img src="./assets/jobintel-logo.png" alt="JobIntel Logo" width="200"> <h1 align="center">JobIntel: </br> The Intelligent Job Market Insights API 🧠💼</h1> </div> <div align="center"> <a href="https://github.com/E-ugine/JobIntel"><img src="https://img.shields.io/badge/GitHub-Repo-000?logo=github&logoColor=white&style=for-the-badge" alt="GitHub Repo"></a> <a href="https://railway.app/"><img src="https://img.shields.io/badge/Deploy-Railway-blue?logo=railway&logoColor=white&style=for-the-badge" alt="Railway Deploy"></a> <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-DB-316192?logo=postgresql&logoColor=white&style=for-the-badge" alt="PostgreSQL"></a> <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=for-the-badge" alt="FastAPI"></a> <a href="https://redis.io/"><img src="https://img.shields.io/badge/Redis-Broker-D92B2B?logo=redis&logoColor=white&style=for-the-badge" alt="Redis"></a> <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Containerized-0db7ed?logo=docker&logoColor=white&style=for-the-badge" alt="Docker"></a> <hr> </div>

Welcome to JobIntel — your AI-powered backend system that continuously scrapes, analyzes, and visualizes job market trends in real-time.
It’s built to empower researchers, hiring teams, and career platforms with live insights into the ever-evolving tech landscape.

✨ Key Features

🚀 Automated Job Scraper — Collects job listings from RemoteOK using Playwright.

🧩 Data Normalization Engine — Cleans and structures unstructured job listings.

🧠 Real-Time Analytics — Tracks skills, salaries, trends, and market shifts.

⚙️ Asynchronous Processing — Powered by Celery workers + Redis.

🧰 Dockerized Stack — One command to spin up API, Worker, Beat, Postgres & Redis.

📊 Interactive Dashboards — See top skills, salary ranges, and hiring velocity.

🔁 Self-Updating System — Beat scheduler keeps your dataset fresh — hands-free.

🚀 Transform messy job listings into clean, queryable intelligence — fully automated.

🔥 News
<div class="scrollable"> <ul> <li><strong>[2025, Oct 17]</strong>: 🎉🎉 <em>JobIntel officially containerized!</em> Full Docker Compose setup now includes API, Celery Worker, Beat, PostgreSQL, and Redis — deployed seamlessly to Railway.</li> <li><strong>[2025, Oct 10]</strong>: 💾 Added RedBeat scheduler for persistent task orchestration in Redis.</li> <li><strong>[2025, Oct 5]</strong>: 🧩 Insights API launched — visualize top skills, salaries, and job title trends.</li> </ul> </div>
📑 Table of Contents

<a href="#overview">📖 Overview</a>

<a href="#architecture">🏗️ Architecture</a>

<a href="#stack">🧰 Tech Stack</a>

<a href="#quick-start">⚡ Quick Start</a>

<a href="#deployment">🚀 Deployment (Railway)</a>

<a href="#api-endpoints">🧠 API Endpoints</a>

<a href="#troubleshooting">🧯 Troubleshooting</a>

<a href="#roadmap">🗺️ Roadmap</a>

<a href="#acknowledgements">🙏 Acknowledgements</a>

<span id="overview"/>
📖 Overview

Job data today is scattered across dozens of platforms, inconsistent in structure, and hard to analyze.
JobIntel automates the full data pipeline:

Scrapes jobs from RemoteOK (and other sources coming soon).

Cleans and standardizes the data with SQLAlchemy.

Stores it in PostgreSQL.

Processes asynchronously via Celery & Redis.

Exposes insights through a FastAPI REST interface and dashboard.

🌀 It’s a self-updating backend that never sleeps.

<span id="architecture"/>
🏗️ Architecture
Layer	Description
FastAPI	REST API & dashboards
Celery Worker	Handles async scraping & ingestion
Celery Beat	Schedules scraping cycles
Redis (RedBeat)	Message broker & Beat scheduler
PostgreSQL	Persistent structured data storage
Docker Compose	Orchestrates all services for local & cloud environments
<span id="stack"/>
🧰 Tech Stack
Category	Tools
Backend	FastAPI, SQLAlchemy, Alembic
Async Tasks	Celery, Redis, RedBeat
Scraping	Playwright
Database	PostgreSQL
Infra	Docker, Railway
Frontend (Dashboards)	Jinja2, Chart.js, TailwindCSS
<span id="quick-start"/>
⚡ Quick Start (Dockerized)
🧱 Prerequisites

Docker & Docker Compose installed

Git

Internet (Playwright pulls Chromium drivers)

🧩 1. Clone
git clone https://github.com/E-ugine/JobIntel.git
cd JobIntel

⚙️ 2. Configure Environment

Create .env:

DATABASE_URL=postgresql://postgres:postgres@db:5432/jobintel
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key
ENV=dev

🐋 3. Build & Run
docker compose up --build


Runs migrations

Launches API, Worker, Beat, DB, and Redis

Accessible at: http://localhost:8000

🧠 4. Trigger a Scrape
curl -X POST http://localhost:8000/api/scrape

📊 5. Access Dashboards
URL	Description
/dashboard	Monitor scrape jobs & performance
/insights	Visualize top skills, salaries, titles
<span id="deployment"/>
🚀 Deployment (Railway)
🔧 Setup

Create a new Railway project → “Deploy from GitHub”

Add PostgreSQL and Redis plugins

Configure three services:

API →

bash -c "python -m alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"


Worker →

celery -A app.core.celery_app.celery worker --loglevel=info


Beat →

celery -A app.core.celery_app.celery beat --loglevel=info


Map env vars:

DATABASE_URL → from Railway Postgres

REDIS_URL → from Railway Redis

SECRET_KEY → set manually

✅ Done — JobIntel now self-updates live on the cloud.

<span id="api-endpoints"/>
🧠 API Endpoints
Endpoint	Method	Description
/api/scrape	POST	Triggers a new scrape cycle
/api/jobs	GET	Fetch all job listings
/api/insights	GET	View analytics summary
/api/stats	GET	Returns scrape statistics
/api/health	GET	Health check
<span id="troubleshooting"/>
🧯 Troubleshooting
Issue	Fix
Playwright Executable Missing	Update Docker base image to mcr.microsoft.com/playwright/python:v1.55.0-jammy
UndefinedTable “jobs”	Run migrations: alembic upgrade head
Beat not scheduling	Ensure RedBeat is enabled in celery_app.py
Worker silent	Check Redis connection and include path in Celery config
<span id="roadmap"/>
🗺️ Roadmap

🌍 Add more job boards (WeWorkRemotely, LinkedIn, Wellfound)

💾 ML-powered skill clustering

📈 Historical salary trends visualization

🔐 Token-based API access

🧩 Deploy frontend dashboard via Next.js

<span id="acknowledgements"/>
🙏 Acknowledgements

This project stands on the shoulders of open-source excellence:
FastAPI, Celery, Redis, SQLAlchemy, Docker, and Playwright — the pillars of modern backend automation.

Built with ❤️ by Eugine Agolla (Charity Wanjiku)

📧 agollaeugine@gmail.com

<a href="#readme-top">⬆️ Back to top</a>