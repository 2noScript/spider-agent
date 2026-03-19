from fastapi import APIRouter

from browser.api import health_check
from browser.api import browser_router
from browser.settings import BrowserSettings, HealthCheckSettings


router = APIRouter()



tags_metadata = [
    {"name": "Health-Check", "description": "**Server Health Check**"},
    {"name": "Browser-Driver", "description": "**Browser-Driver**"}

]


# Health Check routers
router.include_router(
    health_check.router,
    prefix=HealthCheckSettings.router,
    tags=HealthCheckSettings.router_tags,
)


router.include_router(
    browser_router.router,
    prefix=BrowserSettings.router,
    tags=BrowserSettings.router_tags,
)
