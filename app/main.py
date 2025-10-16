from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.jobs import router as jobs_router
from app.api.trends import router as trends_router
from app.api.scrape import router as scrape_router
from app.api.stats import router as stats_router
from app.api.dashboard import router as dashboard_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request


app = FastAPI(title="JobIntel API", version="1.0")

app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(jobs_router, prefix="/api", tags=["Jobs"])
app.include_router(trends_router, prefix="/api", tags=["Trends"])
app.include_router(scrape_router, prefix="/api", tags=["Scraper"])
app.include_router(stats_router, prefix="/api", tags=["Analytics"])
app.include_router(dashboard_router, tags=["Dashboard"])

# Static & template setup
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
