from contextlib import asynccontextmanager
from fastapi import FastAPI
from browser.settings import FastAPISettings
from browser.api.router import router as api_router, tags_metadata

@asynccontextmanager
async def lifespan(application: FastAPI):
    pass


app = FastAPI(
    title=FastAPISettings.title,
    description=FastAPISettings.description,
    version=FastAPISettings.version,
    openapi_tags=tags_metadata,
    docs_url=FastAPISettings.docs_url,
    debug=FastAPISettings.debug,
    # lifespan=lifespan,
)

app.include_router(api_router, prefix="/api")