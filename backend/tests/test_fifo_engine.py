"""Unit tests for the FIFO lot tracking engine."""

from decimal import Decimal

from app.utils.fifo_engine import calculate_fifo
from tests.factories import make_tx


class TestFIFOEngine:
    def test_single_buy(self):
        """Single buy creates one lot with correct quantity."""
        result = calculate_fifo([make_tx("T1", "buy", "100", "50")])

        assert result.current_quantity == Decimal("100")
        assert result.average_cost == Decimal("50")
        assert result.realized_pnl == Decimal("0")
        assert len(result.lots) == 1
        assert result.lots[0].remaining_qty == Decimal("100")

    def test_buy_then_full_sell(self):
        """Full sell of a single lot produces correct realized P&L."""
        txs = [
            make_tx("T1", "buy", "100", "50"),
            make_tx("T2", "sell", "100", "60"),
        ]
        result = calculate_fifo(txs)

        assert result.current_quantity == Decimal("0")
        assert result.realized_pnl == Decimal("1000")  # (60-50) * 100
        assert len(result.lots) == 0

    def test_partial_sell(self):
        """Partial sell leaves remaining lot quantity."""
        txs = [
            make_tx("T1", "buy", "100", "50"),
            make_tx("T2", "sell", "40", "60"),
        ]
        result = calculate_fifo(txs)

        assert result.current_quantity == Decimal("60")
        assert result.realized_pnl == Decimal("400")  # (60-50) * 40
        assert len(result.lots) == 1
        assert result.lots[0].remaining_qty == Decimal("60")

    def test_multi_lot_fifo_order(self):
        """Sells consume oldest lots first (FIFO)."""
        txs = [
            make_tx("T1", "buy", "50", "40"),   # lot 1: 50 @ 40
            make_tx("T2", "buy", "50", "60"),   # lot 2: 50 @ 60
            make_tx("T3", "sell", "70", "55"),   # sells 50 from lot1 + 20 from lot2
        ]
        result = calculate_fifo(txs)

        # P&L: (55-40)*50 + (55-60)*20 = 750 + (-100) = 650
        assert result.realized_pnl == Decimal("650")
        assert result.current_quantity == Decimal("30")
        assert len(result.lots) == 1
        assert result.lots[0].remaining_qty == Decimal("30")
        assert result.lots[0].cost_per_unit == Decimal("60")

    def test_short_sell_detection(self):
        """Selling more than available is flagged as short selling."""
        txs = [
            make_tx("T1", "buy", "50", "100"),
            make_tx("T2", "sell", "80", "110"),
        ]
        result = calculate_fifo(txs)

        assert len(result.short_sells) == 1
        assert result.short_sells[0]["transaction_id"] == "T2"
        assert result.short_sells[0]["short_amount"] == "30"

    def test_empty_transactions(self):
        """No transactions returns zero state."""
        result = calculate_fifo([])

        assert result.current_quantity == Decimal("0")
        assert result.realized_pnl == Decimal("0")
        assert result.average_cost == Decimal("0")

    def test_sell_at_loss(self):
        """Selling at a loss produces negative realized P&L."""
        txs = [
            make_tx("T1", "buy", "100", "80"),
            make_tx("T2", "sell", "100", "70"),
        ]
        result = calculate_fifo(txs)

        assert result.realized_pnl == Decimal("-1000")  # (70-80) * 100

    def test_average_cost_with_multiple_lots(self):
        """Average cost is weighted by remaining lot quantities."""
        txs = [
            make_tx("T1", "buy", "100", "40"),
            make_tx("T2", "buy", "100", "60"),
        ]
        result = calculate_fifo(txs)

        assert result.current_quantity == Decimal("200")
        # Weighted avg: (100*40 + 100*60) / 200 = 50
        assert result.average_cost == Decimal("50")
