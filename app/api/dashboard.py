from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import httpx
import os

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

@router.get("/dashboard")
async def dashboard(request: Request):
    async with httpx.AsyncClient() as client:
        logs_resp = await client.get(f"{API_BASE}/api/logs?limit=20")
        stats_resp = await client.get(f"{API_BASE}/api/stats")

    logs = logs_resp.json()
    stats = stats_resp.json()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "logs": logs, "stats": stats}
    )
