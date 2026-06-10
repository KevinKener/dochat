from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.config import get_settings
from core.logging import configure_logging, get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger = get_logger("main")
    settings = get_settings()
    logger.info("startup", environment=settings.environment, model=settings.anthropic_model)
    yield
    logger.info("shutdown")


app = FastAPI(
    title="DocChat",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    """Return service health status."""
    settings = get_settings()
    return {"status": "ok", "environment": settings.environment}
