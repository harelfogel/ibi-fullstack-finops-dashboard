"""Portfolio response schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PositionOut(BaseModel):
    isin: str
    current_quantity: Decimal
    average_cost: Decimal
    total_invested: Decimal
    realized_pnl: Decimal
    unrealized_pnl: Decimal
    market_value: Decimal
    last_calculated_at: datetime

    model_config = {"from_attributes": True}


class PortfolioOut(BaseModel):
    client_id: str
    positions: list[PositionOut]
    total_value: Decimal
    total_realized_pnl: Decimal
    total_unrealized_pnl: Decimal
