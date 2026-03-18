from fastapi import APIRouter

from browser.api import health_check
from browser.settings import HealthCheckSettings


router = APIRouter()



tags_metadata = [
    {"name": "Health-Check", "description": "**Server Health Check**"}
]


# Health Check routers
router.include_router(
    health_check.router,
    prefix=HealthCheckSettings.router,
    tags=HealthCheckSettings.router_tags,
)
