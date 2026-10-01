from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.logging_config import setup_logging
from app.database import engine, Base
from app.exceptions import (
    CaseNotFoundException,
    case_not_found_handler,
    validation_exception_handler,
    generic_exception_handler
)
from app.api.routes import health, cases

# Configure structured logging
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup and shutdown events."""
    logger.info(f"Starting {settings.APP_NAME} in '{settings.ENVIRONMENT}' environment...")
    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified/created successfully.")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    description="A modular, testable Python REST API backend for managing customer and operational cases.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Exception Handlers
app.add_exception_handler(CaseNotFoundException, case_not_found_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Register Routers
app.include_router(health.router)
app.include_router(cases.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
