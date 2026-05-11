"""AI insight endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.exceptions import NotFoundError
from app.models.client import Client
from app.schemas.base import ApiResponse
from app.schemas.insight import InsightOut
from app.services.insight_service import get_client_insights

router = APIRouter(prefix="/clients", tags=["insights"])


@router.get("/{client_id}/insights", response_model=ApiResponse[InsightOut])
def get_insights(client_id: str, db: Session = Depends(get_db)):
    """Get AI-generated portfolio insights for a client."""
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise NotFoundError(f"Client '{client_id}' not found")

    insights = get_client_insights(client_id, db)
    return ApiResponse(success=True, data=InsightOut(**insights))
