"""Portfolio calculation service using FIFO P&L."""

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.client import Client
from app.models.portfolio_position import PortfolioPosition
from app.models.transaction import Transaction
from app.utils.fifo_engine import FIFOResult, TransactionInput, calculate_fifo


def recalculate_portfolio(client_id: str, db: Session) -> list[PortfolioPosition]:
    """Recalculate all portfolio positions for a client using FIFO.

    Fetches all transactions for the client, groups by ISIN,
    runs the FIFO engine on each group, and upserts PortfolioPosition rows.

    Args:
        client_id: The client identifier.
        db: Database session.

    Returns:
        List of updated PortfolioPosition records.
    """
    transactions = (
        db.query(Transaction)
        .filter(Transaction.client_id == client_id)
        .order_by(Transaction.timestamp.asc())
        .all()
    )

    # Group transactions by ISIN
    isin_groups: dict[str, list[Transaction]] = {}
    for tx in transactions:
        isin_groups.setdefault(tx.isin, []).append(tx)

    now = datetime.now(timezone.utc)
    positions: list[PortfolioPosition] = []

    for isin, txs in isin_groups.items():
        # Convert to FIFO engine input
        fifo_inputs = [
            TransactionInput(
                transaction_id=tx.transaction_id,
                action=tx.action,
                quantity=tx.quantity,
                price=tx.price,
            )
            for tx in txs
        ]

        result: FIFOResult = calculate_fifo(fifo_inputs)

        # Use last transaction price as proxy for market price
        last_price = txs[-1].price
        market_value = result.current_quantity * last_price
        unrealized_pnl = market_value - (result.current_quantity * result.average_cost)

        # Upsert position
        position = (
            db.query(PortfolioPosition)
            .filter(
                PortfolioPosition.client_id == client_id,
                PortfolioPosition.isin == isin,
            )
            .first()
        )

        if position is None:
            position = PortfolioPosition(client_id=client_id, isin=isin)
            db.add(position)

        position.current_quantity = result.current_quantity
        position.average_cost = result.average_cost
        position.total_invested = result.total_invested
        position.realized_pnl = result.realized_pnl
        position.unrealized_pnl = unrealized_pnl
        position.market_value = market_value
        position.last_calculated_at = now

        positions.append(position)

    db.flush()
    return positions


def get_client_portfolio(client_id: str, db: Session) -> list[PortfolioPosition]:
    """Get portfolio positions for a client.

    Args:
        client_id: The client identifier.
        db: Database session.

    Returns:
        List of PortfolioPosition records.

    Raises:
        NotFoundError: If client does not exist.
    """
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise NotFoundError(f"Client '{client_id}' not found")

    return (
        db.query(PortfolioPosition)
        .filter(PortfolioPosition.client_id == client_id)
        .all()
    )


def get_portfolio_summary(client_id: str, db: Session) -> dict:
    """Get aggregated portfolio summary for a client.

    Returns:
        Dict with total_value, total_realized_pnl, total_unrealized_pnl, position_count.
    """
    positions = get_client_portfolio(client_id, db)

    total_value = sum((p.market_value for p in positions), Decimal("0"))
    total_realized = sum((p.realized_pnl for p in positions), Decimal("0"))
    total_unrealized = sum((p.unrealized_pnl for p in positions), Decimal("0"))

    return {
        "total_value": total_value,
        "total_realized_pnl": total_realized,
        "total_unrealized_pnl": total_unrealized,
        "position_count": len(positions),
    }
