"""Unit tests for the validation service."""

from unittest.mock import MagicMock

import pandas as pd
import pytest

from app.services.validation_service import validate_transactions


def _make_df(rows: list[dict]) -> pd.DataFrame:
    """Helper to create a DataFrame with correct column names."""
    return pd.DataFrame(rows)


@pytest.fixture
def mock_db():
    """Mock database session that returns no existing transactions."""
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = []
    return db


class TestValidationService:
    def test_valid_rows_pass(self, mock_db):
        """Valid rows are accepted without errors."""
        df = _make_df([
            {
                "transaction_id": "T001",
                "client_id": "C001",
                "isin": "US1234567890",
                "action": "buy",
                "quantity": 100,
                "price": 50.0,
                "timestamp": "2023-11-01T10:00:00",
            }
        ])
        result = validate_transactions(df, mock_db)

        assert result.is_valid
        assert len(result.valid_rows) == 1
        assert result.total_rows == 1

    def test_negative_quantity_rejected(self, mock_db):
        """Negative quantity produces an error."""
        df = _make_df([
            {
                "transaction_id": "T001",
                "client_id": "C001",
                "isin": "US1234567890",
                "action": "buy",
                "quantity": -10,
                "price": 50.0,
                "timestamp": "2023-11-01T10:00:00",
            }
        ])
        result = validate_transactions(df, mock_db)

        assert not result.is_valid
        assert any(e.field == "quantity" for e in result.errors)

    def test_zero_price_rejected(self, mock_db):
        """Zero price is rejected."""
        df = _make_df([
            {
                "transaction_id": "T001",
                "client_id": "C001",
                "isin": "US1234567890",
                "action": "buy",
                "quantity": 100,
                "price": 0,
                "timestamp": "2023-11-01T10:00:00",
            }
        ])
        result = validate_transactions(df, mock_db)

        assert not result.is_valid
        assert any(e.field == "price" for e in result.errors)

    def test_invalid_action_rejected(self, mock_db):
        """Invalid action value is rejected."""
        df = _make_df([
            {
                "transaction_id": "T001",
                "client_id": "C001",
                "isin": "US1234567890",
                "action": "hold",
                "quantity": 100,
                "price": 50.0,
                "timestamp": "2023-11-01T10:00:00",
            }
        ])
        result = validate_transactions(df, mock_db)

        assert not result.is_valid
        assert any(e.field == "action" for e in result.errors)

    def test_duplicate_tx_ids_in_batch(self, mock_db):
        """Duplicate transaction IDs within a batch are detected."""
        df = _make_df([
            {
                "transaction_id": "T001",
                "client_id": "C001",
                "isin": "US1234567890",
                "action": "buy",
                "quantity": 100,
                "price": 50.0,
                "timestamp": "2023-11-01T10:00:00",
            },
            {
                "transaction_id": "T001",
                "client_id": "C002",
                "isin": "US0987654321",
                "action": "sell",
                "quantity": 50,
                "price": 60.0,
                "timestamp": "2023-11-02T10:00:00",
            },
        ])
        result = validate_transactions(df, mock_db)

        # First row valid, second has duplicate
        assert len(result.valid_rows) == 1
        assert len(result.errors) == 1
        assert "Duplicate" in result.errors[0].message

    def test_invalid_isin_format(self, mock_db):
        """ISIN with wrong format is rejected."""
        df = _make_df([
            {
                "transaction_id": "T001",
                "client_id": "C001",
                "isin": "INVALID",
                "action": "buy",
                "quantity": 100,
                "price": 50.0,
                "timestamp": "2023-11-01T10:00:00",
            }
        ])
        result = validate_transactions(df, mock_db)

        assert not result.is_valid
        assert any(e.field == "isin" for e in result.errors)

    def test_missing_client_id(self, mock_db):
        """Missing client ID is rejected."""
        df = _make_df([
            {
                "transaction_id": "T001",
                "client_id": float("nan"),
                "isin": "US1234567890",
                "action": "buy",
                "quantity": 100,
                "price": 50.0,
                "timestamp": "2023-11-01T10:00:00",
            }
        ])
        result = validate_transactions(df, mock_db)

        assert not result.is_valid
        assert any(e.field == "client_id" for e in result.errors)

    def test_multiple_valid_rows(self, mock_db):
        """Multiple valid rows all pass."""
        df = _make_df([
            {
                "transaction_id": f"T00{i}",
                "client_id": "C001",
                "isin": "US1234567890",
                "action": "buy",
                "quantity": 100,
                "price": 50.0,
                "timestamp": f"2023-11-0{i}T10:00:00",
            }
            for i in range(1, 4)
        ])
        result = validate_transactions(df, mock_db)

        assert result.is_valid
        assert len(result.valid_rows) == 3
