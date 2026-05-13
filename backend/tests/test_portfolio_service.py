"""Integration tests for the portfolio service."""

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.transaction import Transaction
from app.services.portfolio_service import get_portfolio_summary, recalculate_portfolio


def _seed_client(db: Session, client_id: str) -> None:
    db.add(Client(client_id=client_id))
    db.flush()


def _seed_tx(
    db: Session, tx_id: str, client_id: str, isin: str,
    action: str, qty: Decimal, price: Decimal, ts: datetime,
) -> None:
    db.add(
        Transaction(
            transaction_id=tx_id, client_id=client_id, isin=isin,
            action=action, quantity=qty, price=price, timestamp=ts,
            upload_batch_id=uuid.uuid4(),
        )
    )
    db.flush()


class TestPortfolioRecalculation:
    def test_single_buy_position(self, db: Session):
        """Single buy creates a position with correct values."""
        _seed_client(db, "C001")
        _seed_tx(db, "T1", "C001", "US1234567890", "buy",
                 Decimal("100"), Decimal("50"), datetime(2023, 11, 1, tzinfo=timezone.utc))

        positions = recalculate_portfolio("C001", db)

        assert len(positions) == 1
        pos = positions[0]
        assert pos.isin == "US1234567890"
        assert pos.current_quantity == Decimal("100")
        assert pos.average_cost == Decimal("50")
        assert pos.realized_pnl == Decimal("0")

    def test_buy_sell_realized_pnl(self, db: Session):
        """Buy then sell produces realized P&L."""
        _seed_client(db, "C001")
        base = datetime(2023, 11, 1, tzinfo=timezone.utc)
        _seed_tx(db, "T1", "C001", "US1234567890", "buy",
                 Decimal("100"), Decimal("50"), base)
        _seed_tx(db, "T2", "C001", "US1234567890", "sell",
                 Decimal("40"), Decimal("60"), base + timedelta(days=1))

        positions = recalculate_portfolio("C001", db)

        assert len(positions) == 1
        pos = positions[0]
        assert pos.current_quantity == Decimal("60")
        assert pos.realized_pnl == Decimal("400")  # (60-50)*40

    def test_multiple_isins(self, db: Session):
        """Transactions across ISINs create separate positions."""
        _seed_client(db, "C001")
        base = datetime(2023, 11, 1, tzinfo=timezone.utc)
        _seed_tx(db, "T1", "C001", "US1234567890", "buy",
                 Decimal("100"), Decimal("50"), base)
        _seed_tx(db, "T2", "C001", "US0987654321", "buy",
                 Decimal("200"), Decimal("30"), base + timedelta(days=1))

        positions = recalculate_portfolio("C001", db)

        assert len(positions) == 2
        isins = {p.isin for p in positions}
        assert isins == {"US1234567890", "US0987654321"}

    def test_portfolio_summary(self, db: Session):
        """Portfolio summary aggregates across positions."""
        _seed_client(db, "C001")
        base = datetime(2023, 11, 1, tzinfo=timezone.utc)
        _seed_tx(db, "T1", "C001", "US1234567890", "buy",
                 Decimal("100"), Decimal("50"), base)
        _seed_tx(db, "T2", "C001", "US0987654321", "buy",
                 Decimal("200"), Decimal("30"), base + timedelta(days=1))

        recalculate_portfolio("C001", db)
        db.commit()

        summary = get_portfolio_summary("C001", db)

        assert summary["position_count"] == 2
        assert summary["total_value"] > 0
