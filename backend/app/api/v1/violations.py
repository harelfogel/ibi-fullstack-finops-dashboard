"""Violation endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.exceptions import NotFoundError
from app.models.client import Client
from app.schemas.base import ApiResponse
from app.schemas.violation import ViolationOut
from app.services.violation_service import get_client_violations

router = APIRouter(prefix="/clients", tags=["violations"])


@router.get("/{client_id}/violations", response_model=ApiResponse[list[ViolationOut]])
def get_violations(client_id: str, db: Session = Depends(get_db)):
    """Get all violations for a client."""
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise NotFoundError(f"Client '{client_id}' not found")

    violations = get_client_violations(client_id, db)
    items = [ViolationOut.model_validate(v) for v in violations]
    return ApiResponse(success=True, data=items)
