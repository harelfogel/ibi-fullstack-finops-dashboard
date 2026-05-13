"""Unit tests for the violation detection service."""

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.portfolio_position import PortfolioPosition
from app.models.transaction import Transaction
from app.services.violation_service import detect_violations


def _seed_client(db: Session, client_id: str = "C001") -> None:
    """Create a client in the test database."""
    db.add(Client(client_id=client_id))
    db.flush()


def _seed_transaction(
    db: Session,
    tx_id: str,
    client_id: str,
    isin: str,
    action: str,
    quantity: Decimal,
    price: Decimal,
    timestamp: datetime,
) -> None:
    """Create a transaction in the test database."""
    db.add(
        Transaction(
            transaction_id=tx_id,
            client_id=client_id,
            isin=isin,
            action=action,
            quantity=quantity,
            price=price,
            timestamp=timestamp,
            upload_batch_id=uuid.uuid4(),
        )
    )
    db.flush()


def _seed_position(
    db: Session,
    client_id: str,
    isin: str,
    market_value: Decimal,
    current_quantity: Decimal = Decimal("100"),
) -> None:
    """Create a portfolio position in the test database."""
    db.add(
        PortfolioPosition(
            client_id=client_id,
            isin=isin,
            current_quantity=current_quantity,
            average_cost=Decimal("50"),
            total_invested=Decimal("5000"),
            realized_pnl=Decimal("0"),
            unrealized_pnl=Decimal("0"),
            market_value=market_value,
            last_calculated_at=datetime.now(timezone.utc),
        )
    )
    db.flush()


class TestShortSellingDetection:
    def test_short_sell_detected(self, db: Session):
        """Selling more than available triggers short-selling violation."""
        _seed_client(db, "C001")
        base = datetime(2023, 11, 1, tzinfo=timezone.utc)
        _seed_transaction(
            db, "T1", "C001", "US1234567890", "buy",
            Decimal("50"), Decimal("100"), base,
        )
        _seed_transaction(
            db, "T2", "C001", "US1234567890", "sell",
            Decimal("80"), Decimal("110"), base + timedelta(days=1),
        )

        violations = detect_violations("C001", db)

        short_violations = [v for v in violations if v.violation_type == "short_selling"]
        assert len(short_violations) == 1
        assert short_violations[0].severity == "error"

    def test_no_short_sell_when_sufficient(self, db: Session):
        """Selling within available quantity does not trigger violation."""
        _seed_client(db, "C001")
        base = datetime(2023, 11, 1, tzinfo=timezone.utc)
        _seed_transaction(
            db, "T1", "C001", "US1234567890", "buy",
            Decimal("100"), Decimal("100"), base,
        )
        _seed_transaction(
            db, "T2", "C001", "US1234567890", "sell",
            Decimal("50"), Decimal("110"), base + timedelta(days=1),
        )

        violations = detect_violations("C001", db)

        short_violations = [v for v in violations if v.violation_type == "short_selling"]
        assert len(short_violations) == 0


class TestConcentrationRisk:
    def test_concentration_above_threshold(self, db: Session):
        """Position > 50% of portfolio triggers concentration warning."""
        _seed_client(db, "C001")
        _seed_position(db, "C001", "US1234567890", Decimal("8000"))
        _seed_position(db, "C001", "US0987654321", Decimal("2000"))

        violations = detect_violations("C001", db)

        conc_violations = [v for v in violations if v.violation_type == "concentration_risk"]
        assert len(conc_violations) == 1
        assert conc_violations[0].severity == "warning"
        assert "US1234567890" in conc_violations[0].message

    def test_no_concentration_when_balanced(self, db: Session):
        """Balanced portfolio does not trigger concentration warning."""
        _seed_client(db, "C001")
        _seed_position(db, "C001", "US1234567890", Decimal("5000"))
        _seed_position(db, "C001", "US0987654321", Decimal("5000"))

        violations = detect_violations("C001", db)

        conc_violations = [v for v in violations if v.violation_type == "concentration_risk"]
        assert len(conc_violations) == 0


class TestDayTrading:
    def test_day_trading_detected(self, db: Session):
        """3+ buy/sell pairs within 24h triggers day trading warning."""
        _seed_client(db, "C001")
        base = datetime(2023, 11, 1, 10, 0, 0, tzinfo=timezone.utc)

        # Create 3 buy/sell pairs within 24h
        for i in range(3):
            _seed_transaction(
                db, f"B{i}", "C001", "US1234567890", "buy",
                Decimal("10"), Decimal("100"),
                base + timedelta(hours=i),
            )
            _seed_transaction(
                db, f"S{i}", "C001", "US1234567890", "sell",
                Decimal("10"), Decimal("105"),
                base + timedelta(hours=i, minutes=30),
            )

        violations = detect_violations("C001", db)

        dt_violations = [v for v in violations if v.violation_type == "day_trading"]
        assert len(dt_violations) == 1
        assert dt_violations[0].severity == "warning"
