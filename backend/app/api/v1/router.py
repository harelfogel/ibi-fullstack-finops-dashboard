"""Aggregated v1 API router."""

from fastapi import APIRouter

from app.api.v1 import clients, insights, portfolio, transactions, violations

router = APIRouter(prefix="/api/v1")

router.include_router(transactions.router)
router.include_router(clients.router)
router.include_router(portfolio.router)
router.include_router(violations.router)
router.include_router(insights.router)
