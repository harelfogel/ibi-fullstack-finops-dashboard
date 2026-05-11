"""Rule violation detection service."""

from collections import defaultdict
from datetime import timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.constants import (
    CONCENTRATION_RISK_THRESHOLD,
    DAY_TRADING_PAIR_THRESHOLD,
    DAY_TRADING_WINDOW_HOURS,
    ViolationSeverity,
    ViolationType,
)
from app.models.portfolio_position import PortfolioPosition
from app.models.transaction import Transaction
from app.models.violation import Violation


def detect_violations(client_id: str, db: Session) -> list[Violation]:
    """Detect all rule violations for a client and persist them.

    Checks:
    1. Short selling: sell quantity exceeds available holdings (FIFO)
    2. Concentration risk: single ISIN > 50% of portfolio value
    3. Day trading: 3+ buy/sell pairs for same ISIN within 24 hours

    Args:
        client_id: The client identifier.
        db: Database session.

    Returns:
        List of newly created Violation records.
    """
    # Clear previous violations for this client (recalculate fresh)
    db.query(Violation).filter(Violation.client_id == client_id).delete()

    new_violations: list[Violation] = []

    # ── 1. Short selling detection ──────────────────────────────
    new_violations.extend(_detect_short_selling(client_id, db))

    # ── 2. Concentration risk detection ─────────────────────────
    new_violations.extend(_detect_concentration_risk(client_id, db))

    # ── 3. Day trading detection ────────────────────────────────
    new_violations.extend(_detect_day_trading(client_id, db))

    db.add_all(new_violations)
    db.flush()
    return new_violations


def _detect_short_selling(client_id: str, db: Session) -> list[Violation]:
    """Detect sells that exceed available quantity (FIFO-based)."""
    from app.utils.fifo_engine import TransactionInput, calculate_fifo

    violations: list[Violation] = []

    transactions = (
        db.query(Transaction)
        .filter(Transaction.client_id == client_id)
        .order_by(Transaction.timestamp.asc())
        .all()
    )

    # Group by ISIN
    isin_groups: dict[str, list[Transaction]] = {}
    for tx in transactions:
        isin_groups.setdefault(tx.isin, []).append(tx)

    for isin, txs in isin_groups.items():
        fifo_inputs = [
            TransactionInput(
                transaction_id=tx.transaction_id,
                action=tx.action,
                quantity=tx.quantity,
                price=tx.price,
            )
            for tx in txs
        ]
        result = calculate_fifo(fifo_inputs)

        for short in result.short_sells:
            violations.append(
                Violation(
                    client_id=client_id,
                    transaction_id=short["transaction_id"],
                    violation_type=ViolationType.SHORT_SELLING,
                    severity=ViolationSeverity.ERROR,
                    message=(
                        f"Short selling detected on {isin}: attempted to sell "
                        f"{short['sell_quantity']} units but only "
                        f"{short['available_quantity']} available"
                    ),
                    details={"isin": isin, **short},
                )
            )

    return violations


def _detect_concentration_risk(client_id: str, db: Session) -> list[Violation]:
    """Detect when a single ISIN exceeds the concentration threshold."""
    violations: list[Violation] = []

    positions = (
        db.query(PortfolioPosition)
        .filter(PortfolioPosition.client_id == client_id)
        .all()
    )

    total_value = sum((p.market_value for p in positions), Decimal("0"))

    if total_value <= 0:
        return violations

    for position in positions:
        if position.market_value <= 0:
            continue
        concentration = position.market_value / total_value
        if concentration > CONCENTRATION_RISK_THRESHOLD:
            violations.append(
                Violation(
                    client_id=client_id,
                    violation_type=ViolationType.CONCENTRATION_RISK,
                    severity=ViolationSeverity.WARNING,
                    message=(
                        f"Concentration risk: {position.isin} represents "
                        f"{concentration:.1%} of portfolio (threshold: "
                        f"{CONCENTRATION_RISK_THRESHOLD:.0%})"
                    ),
                    details={
                        "isin": position.isin,
                        "concentration": str(concentration),
                        "market_value": str(position.market_value),
                        "total_portfolio_value": str(total_value),
                    },
                )
            )

    return violations


def _detect_day_trading(client_id: str, db: Session) -> list[Violation]:
    """Detect excessive buy/sell pairs within the day-trading window."""
    violations: list[Violation] = []

    transactions = (
        db.query(Transaction)
        .filter(Transaction.client_id == client_id)
        .order_by(Transaction.timestamp.asc())
        .all()
    )

    # Group by ISIN
    isin_groups: dict[str, list[Transaction]] = defaultdict(list)
    for tx in transactions:
        isin_groups[tx.isin].append(tx)

    window = timedelta(hours=DAY_TRADING_WINDOW_HOURS)

    for isin, txs in isin_groups.items():
        # Count buy/sell pairs within rolling windows
        buys = [tx for tx in txs if tx.action == "buy"]
        sells = [tx for tx in txs if tx.action == "sell"]

        pair_count = 0
        for buy in buys:
            for sell in sells:
                if abs(sell.timestamp - buy.timestamp) <= window:
                    pair_count += 1

        if pair_count >= DAY_TRADING_PAIR_THRESHOLD:
            violations.append(
                Violation(
                    client_id=client_id,
                    violation_type=ViolationType.DAY_TRADING,
                    severity=ViolationSeverity.WARNING,
                    message=(
                        f"Day trading pattern detected on {isin}: "
                        f"{pair_count} buy/sell pairs within "
                        f"{DAY_TRADING_WINDOW_HOURS}h window "
                        f"(threshold: {DAY_TRADING_PAIR_THRESHOLD})"
                    ),
                    details={
                        "isin": isin,
                        "pair_count": pair_count,
                        "window_hours": DAY_TRADING_WINDOW_HOURS,
                    },
                )
            )

    return violations


def get_client_violations(client_id: str, db: Session) -> list[Violation]:
    """Get all violations for a client."""
    return (
        db.query(Violation)
        .filter(Violation.client_id == client_id)
        .order_by(Violation.detected_at.desc())
        .all()
    )
