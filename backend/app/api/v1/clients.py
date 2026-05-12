"""Client endpoints."""

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.exceptions import NotFoundError
from app.models.client import Client
from app.models.portfolio_position import PortfolioPosition
from app.models.transaction import Transaction
from app.models.violation import Violation
from app.schemas.base import ApiResponse
from app.schemas.client import ClientDetail, ClientSummary

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=ApiResponse[list[ClientSummary]])
def list_clients(db: Session = Depends(get_db)):
    """List all clients with portfolio summaries."""
    clients = db.query(Client).order_by(Client.client_id).all()

    summaries = []
    for client in clients:
        positions = (
            db.query(PortfolioPosition)
            .filter(PortfolioPosition.client_id == client.client_id)
            .all()
        )
        violation_count = (
            db.query(Violation)
            .filter(Violation.client_id == client.client_id)
            .count()
        )

        total_value = sum((p.market_value for p in positions), Decimal("0"))
        total_realized = sum((p.realized_pnl for p in positions), Decimal("0"))
        total_unrealized = sum((p.unrealized_pnl for p in positions), Decimal("0"))

        summaries.append(
            ClientSummary(
                client_id=client.client_id,
                position_count=len(positions),
                total_value=total_value,
                total_realized_pnl=total_realized,
                total_unrealized_pnl=total_unrealized,
                violation_count=violation_count,
                created_at=client.created_at,
            )
        )

    return ApiResponse(success=True, data=summaries)


@router.get("/{client_id}", response_model=ApiResponse[ClientDetail])
def get_client(client_id: str, db: Session = Depends(get_db)):
    """Get client details."""
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise NotFoundError(f"Client '{client_id}' not found")

    return ApiResponse(success=True, data=ClientDetail.model_validate(client))


@router.delete("/{client_id}", response_model=ApiResponse[dict])
def delete_client(client_id: str, db: Session = Depends(get_db)):
    """Delete a client and all associated data."""
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise NotFoundError(f"Client '{client_id}' not found")

    # Delete in FK-safe order: violations -> transactions -> positions -> client
    db.query(Violation).filter(Violation.client_id == client_id).delete()
    db.query(Transaction).filter(Transaction.client_id == client_id).delete()
    db.query(PortfolioPosition).filter(
        PortfolioPosition.client_id == client_id
    ).delete()
    db.delete(client)
    db.commit()

    return ApiResponse(success=True, data={"client_id": client_id})
