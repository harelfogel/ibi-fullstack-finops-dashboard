"""Violation response schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ViolationOut(BaseModel):
    id: int
    client_id: str
    transaction_id: str | None
    violation_type: str
    severity: str
    message: str
    details: dict[str, Any] | None
    detected_at: datetime

    model_config = {"from_attributes": True}
