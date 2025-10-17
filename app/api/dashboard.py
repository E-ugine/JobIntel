from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
import os

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

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

@router.get("/insights", response_class=HTMLResponse)
async def insights_page(request: Request):
    return templates.TemplateResponse("insights.html", {"request": request})
