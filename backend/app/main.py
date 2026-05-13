"""FastAPI application entry point."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.v1.router import router as v1_router
from app.config import settings
from app.exceptions import register_exception_handlers

logging.basicConfig(level=settings.LOG_LEVEL)

app = FastAPI(
    title="IBI FinOps Dashboard API",
    description=(
        "Financial operations dashboard backend"
        " - transaction processing, portfolio management, and AI insights."
    ),
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX or None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
register_exception_handlers(app)

# Routers
app.include_router(health_router)
app.include_router(v1_router)
