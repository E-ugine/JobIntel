from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
import os

# Template engine
templates = Jinja2Templates(directory="app/templates")

# Single shared router
router = APIRouter()

# Base API URL (use .env in prod)
API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")


# 🧭 Dashboard (Scraper Health)
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Render the main dashboard with logs + stats."""
    async with httpx.AsyncClient() as client:
        logs_resp = await client.get(f"{API_BASE}/api/logs?limit=20")
        stats_resp = await client.get(f"{API_BASE}/api/stats")

    logs = logs_resp.json() if logs_resp.status_code == 200 else []
    stats = stats_resp.json() if stats_resp.status_code == 200 else {}

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "logs": logs, "stats": stats}
    )


# 💡 Insights (Job Market Analytics)
@router.get("/insights", response_class=HTMLResponse)
async def insights_page(request: Request):
    """Render job market insights dashboard."""
    return templates.TemplateResponse("insights.html", {"request": request})
