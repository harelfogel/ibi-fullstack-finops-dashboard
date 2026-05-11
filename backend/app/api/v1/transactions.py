"""Transaction endpoints."""

import math

from fastapi import APIRouter, Depends, Query, UploadFile
from sqlalchemy.orm import Session

from app.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.models.transaction import Transaction
from app.schemas.base import ApiResponse, PaginationMeta
from app.schemas.transaction import TransactionOut, UploadResult
from app.services.upload_service import process_upload

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/upload", response_model=ApiResponse[UploadResult])
async def upload_transactions(file: UploadFile, db: Session = Depends(get_db)):
    """Upload a CSV/XLSX file of transactions."""
    content = await file.read()
    result = process_upload(file.filename or "unknown.csv", content, db)
    return ApiResponse(success=True, data=UploadResult(**result))


@router.get("", response_model=ApiResponse[list[TransactionOut]])
def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    client_id: str | None = Query(None),
    isin: str | None = Query(None),
    action: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """List transactions with pagination and optional filters."""
    query = db.query(Transaction)

    if client_id:
        query = query.filter(Transaction.client_id == client_id)
    if isin:
        query = query.filter(Transaction.isin == isin)
    if action:
        query = query.filter(Transaction.action == action)

    total = query.count()
    transactions = (
        query.order_by(Transaction.timestamp.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    items = [
        TransactionOut(
            transaction_id=tx.transaction_id,
            client_id=tx.client_id,
            isin=tx.isin,
            action=tx.action,
            quantity=tx.quantity,
            price=tx.price,
            timestamp=tx.timestamp,
            upload_batch_id=str(tx.upload_batch_id),
        )
        for tx in transactions
    ]

    return ApiResponse(
        success=True,
        data=items,
        pagination=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=math.ceil(total / page_size) if total > 0 else 0,
        ),
    )
