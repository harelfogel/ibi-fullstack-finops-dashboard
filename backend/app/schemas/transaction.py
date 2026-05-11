"""Transaction request/response schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TransactionOut(BaseModel):
    transaction_id: str
    client_id: str
    isin: str
    action: str
    quantity: Decimal
    price: Decimal
    timestamp: datetime
    upload_batch_id: str

    model_config = {"from_attributes": True}


class UploadError(BaseModel):
    row: int
    field: str
    message: str


class UploadResult(BaseModel):
    batch_id: str
    total_rows: int
    valid_rows: int
    error_rows: int
    errors: list[UploadError]
    affected_clients: list[str]
