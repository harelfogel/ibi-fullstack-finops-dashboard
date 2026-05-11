"""Client response schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ClientSummary(BaseModel):
    client_id: str
    position_count: int
    total_value: Decimal
    total_realized_pnl: Decimal
    total_unrealized_pnl: Decimal
    violation_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ClientDetail(BaseModel):
    client_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
