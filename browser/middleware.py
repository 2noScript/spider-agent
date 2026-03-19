import time
import traceback
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from fastapi import status

from browser.api.model import ErrorResponseModel
from browser.logging import configure_logging

logger = configure_logging(name="api_logger")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"➡️ {request.method} {request.url.path} from {request.client.host}")

        try:
            response: Response = await call_next(request)

        except Exception as e:
            logger.exception(f"❌ Exception while processing {request.method} {request.url.path}: {str(e)}")
            traceback_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            logger.error(traceback_str)

            error_response = ErrorResponseModel(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e),
            )

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=error_response.model_dump(),
            )

        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"⬅️ {request.method} {request.url.path} "
            f"status={response.status_code} duration={process_time:.2f}ms"
        )

        return response
