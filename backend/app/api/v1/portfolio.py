"""Portfolio endpoints."""

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.base import ApiResponse
from app.schemas.portfolio import PortfolioOut, PositionOut
from app.services.portfolio_service import get_client_portfolio

router = APIRouter(prefix="/clients", tags=["portfolio"])


@router.get("/{client_id}/portfolio", response_model=ApiResponse[PortfolioOut])
def get_portfolio(client_id: str, db: Session = Depends(get_db)):
    """Get detailed portfolio for a client with FIFO-calculated positions."""
    positions = get_client_portfolio(client_id, db)

    position_items = [PositionOut.model_validate(p) for p in positions]

    total_value = sum((p.market_value for p in positions), Decimal("0"))
    total_realized = sum((p.realized_pnl for p in positions), Decimal("0"))
    total_unrealized = sum((p.unrealized_pnl for p in positions), Decimal("0"))

    return ApiResponse(
        success=True,
        data=PortfolioOut(
            client_id=client_id,
            positions=position_items,
            total_value=total_value,
            total_realized_pnl=total_realized,
            total_unrealized_pnl=total_unrealized,
        ),
    )
