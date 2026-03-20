from typing import Union

from fastapi import APIRouter

from browser.api.model import ErrorResponseModel, ResponseModel
from browser.engine.core.const import SUPPORT_BROWSER
from browser.logging import configure_logging


router = APIRouter()
logger = configure_logging(name=__name__)


@router.get("/status")
async def fetch_status() -> Union[ResponseModel, ErrorResponseModel]:
    pass


@router.get("/support_type")
async def fetch_browser_support() -> Union[ResponseModel, ErrorResponseModel]:
    return ResponseModel(data=SUPPORT_BROWSER)
