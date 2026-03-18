from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class HealthCheckResponse(BaseModel):
    status: str = "ok"


@router.get(
    "/check",
    summary="Check if the server responds to requests correctly",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Server responds successfully",
            "content": {"application/json": {"example": {"status": "ok"}}},
        }
    },
)
async def health_check():

    return HealthCheckResponse()


