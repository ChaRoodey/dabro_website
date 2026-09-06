from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.router import router
from app.core.config import settings
from app.core.logging import setup_logger, get_logger

setup_logger()
logger = get_logger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App started")
    yield
    logger.info("App stopped")


app = FastAPI(
    lifespan=lifespan,
    docs_url='/docs' if settings.LOG_LEVEL == 'DEBUG' else None,
    redoc_url='/redoc' if settings.LOG_LEVEL == 'DEBUG' else None,
    openapi_url='/openapi.json' if settings.LOG_LEVEL == 'DEBUG' else None,
)

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
