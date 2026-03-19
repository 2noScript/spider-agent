from typing import Union

from fastapi import APIRouter

from browser.api.model import ErrorResponseModel, ResponseModel
from browser.logging import configure_logging



router = APIRouter()
logger = configure_logging(name=__name__)


@router.get("/status")
async def fetch_status()-> Union[ResponseModel, ErrorResponseModel]:
    pass

