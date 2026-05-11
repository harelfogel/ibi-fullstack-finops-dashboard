"""FIFO (First In, First Out) lot tracking engine.

Pure functions - no database or side-effect dependencies.
"""

from collections import deque
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Lot:
    """A buy lot in the FIFO queue."""

    transaction_id: str
    remaining_qty: Decimal
    cost_per_unit: Decimal


@dataclass
class FIFOResult:
    """Result of running the FIFO engine over a sequence of transactions."""

    lots: list[Lot] = field(default_factory=list)
    realized_pnl: Decimal = Decimal("0")
    current_quantity: Decimal = Decimal("0")
    average_cost: Decimal = Decimal("0")
    total_invested: Decimal = Decimal("0")
    short_sells: list[dict] = field(default_factory=list)


@dataclass
class TransactionInput:
    """Minimal transaction data needed by the FIFO engine."""

    transaction_id: str
    action: str  # "buy" or "sell"
    quantity: Decimal
    price: Decimal


def calculate_fifo(transactions: list[TransactionInput]) -> FIFOResult:
    """Calculate portfolio position using FIFO lot tracking.

    Args:
        transactions: Chronologically ordered list of transactions for a single
                      client+ISIN pair.

    Returns:
        FIFOResult with remaining lots, realized P&L, and short-sell detections.
    """
    queue: deque[Lot] = deque()
    realized_pnl = Decimal("0")
    total_invested = Decimal("0")
    short_sells: list[dict] = []

    for tx in transactions:
        if tx.action == "buy":
            queue.append(
                Lot(
                    transaction_id=tx.transaction_id,
                    remaining_qty=tx.quantity,
                    cost_per_unit=tx.price,
                )
            )
            total_invested += tx.quantity * tx.price

        elif tx.action == "sell":
            sell_remaining = tx.quantity
            available_qty = sum(lot.remaining_qty for lot in queue)

            if sell_remaining > available_qty:
                short_sells.append(
                    {
                        "transaction_id": tx.transaction_id,
                        "sell_quantity": str(sell_remaining),
                        "available_quantity": str(available_qty),
                        "short_amount": str(sell_remaining - available_qty),
                    }
                )

            # Consume lots from front of queue (FIFO)
            while sell_remaining > 0 and queue:
                lot = queue[0]
                consumed = min(lot.remaining_qty, sell_remaining)
                realized_pnl += (tx.price - lot.cost_per_unit) * consumed
                lot.remaining_qty -= consumed
                sell_remaining -= consumed

                if lot.remaining_qty == 0:
                    queue.popleft()

    # Calculate current state
    remaining_lots = list(queue)
    current_quantity = sum(lot.remaining_qty for lot in remaining_lots)

    if current_quantity > 0:
        total_cost = sum(lot.remaining_qty * lot.cost_per_unit for lot in remaining_lots)
        average_cost = total_cost / current_quantity
    else:
        average_cost = Decimal("0")

    return FIFOResult(
        lots=remaining_lots,
        realized_pnl=realized_pnl,
        current_quantity=current_quantity,
        average_cost=average_cost,
        total_invested=total_invested,
        short_sells=short_sells,
    )
