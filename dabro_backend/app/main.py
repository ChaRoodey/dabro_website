from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.router import router
from app.core.config import settings
from app.core.logging import setup_logger, get_logger
from app.core.metrix_middleware import metrics_and_visitors_middleware

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

Instrumentator(excluded_handlers=["/metrics"], ).instrument(app).expose(app, endpoint="/metrics")
app.include_router(router)
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.middleware("http")(metrics_and_visitors_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
