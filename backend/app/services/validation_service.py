"""Transaction data validation service."""

import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

import pandas as pd
from sqlalchemy.orm import Session

from app.constants import ISIN_LENGTH, TransactionAction
from app.models.transaction import Transaction


@dataclass
class RowError:
    """A single validation error on a specific row."""

    row: int
    field: str
    message: str


@dataclass
class ValidationResult:
    """Result of validating an upload batch."""

    valid_rows: list[dict] = field(default_factory=list)
    errors: list[RowError] = field(default_factory=list)

    @property
    def total_rows(self) -> int:
        return len(self.valid_rows) + len(self.errors)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


ISIN_PATTERN = re.compile(r"^[A-Z]{2}[A-Z0-9]{10}$")


def validate_transactions(df: pd.DataFrame, db: Session) -> ValidationResult:
    """Validate all rows in the uploaded DataFrame.

    Checks:
    - Required fields present and non-null
    - Quantity > 0
    - Price > 0
    - Action is 'buy' or 'sell'
    - ISIN format (2 letter country + 10 alphanumeric)
    - Transaction IDs unique within batch
    - Transaction IDs not already in database

    Args:
        df: Normalized DataFrame from csv_parser.
        db: Database session for duplicate checking.

    Returns:
        ValidationResult with valid rows and any errors.
    """
    result = ValidationResult()
    seen_tx_ids: set[str] = set()

    # Check existing transaction IDs in database
    incoming_tx_ids = df["transaction_id"].dropna().astype(str).tolist()
    existing_ids: set[str] = set()
    if incoming_tx_ids:
        existing = (
            db.query(Transaction.transaction_id)
            .filter(Transaction.transaction_id.in_(incoming_tx_ids))
            .all()
        )
        existing_ids = {row[0] for row in existing}

    for idx, row in df.iterrows():
        row_num = int(idx) + 2  # +2 for 1-indexed + header row
        row_errors: list[RowError] = []

        # Transaction ID
        tx_id = str(row.get("transaction_id", "")).strip()
        if not tx_id or tx_id == "nan":
            row_errors.append(RowError(row_num, "transaction_id", "Missing transaction ID"))
        elif tx_id in seen_tx_ids:
            row_errors.append(
                RowError(row_num, "transaction_id", f"Duplicate transaction ID '{tx_id}' in batch")
            )
        elif tx_id in existing_ids:
            row_errors.append(
                RowError(
                    row_num,
                    "transaction_id",
                    f"Transaction ID '{tx_id}' already exists in database",
                )
            )
        else:
            seen_tx_ids.add(tx_id)

        # Client ID
        client_id = str(row.get("client_id", "")).strip()
        if not client_id or client_id == "nan":
            row_errors.append(RowError(row_num, "client_id", "Missing client ID"))

        # ISIN
        isin = str(row.get("isin", "")).strip()
        if not isin or isin == "nan":
            row_errors.append(RowError(row_num, "isin", "Missing ISIN"))
        elif len(isin) != ISIN_LENGTH or not ISIN_PATTERN.match(isin):
            row_errors.append(
                RowError(
                    row_num,
                    "isin",
                    f"Invalid ISIN format '{isin}'"
                    f" (expected {ISIN_LENGTH} chars,"
                    " 2 letters + 10 alphanumeric)",
                )
            )

        # Action
        action = str(row.get("action", "")).strip().lower()
        valid_actions = {a.value for a in TransactionAction}
        if action not in valid_actions:
            row_errors.append(
                RowError(
                    row_num,
                    "action",
                    f"Invalid action '{action}'."
                    f" Must be one of: {', '.join(valid_actions)}",
                )
            )

        # Quantity
        try:
            quantity = Decimal(str(row.get("quantity", "")))
            if quantity <= 0:
                row_errors.append(RowError(row_num, "quantity", "Quantity must be greater than 0"))
        except (InvalidOperation, ValueError):
            row_errors.append(RowError(row_num, "quantity", "Invalid quantity value"))

        # Price
        try:
            price = Decimal(str(row.get("price", "")))
            if price <= 0:
                row_errors.append(RowError(row_num, "price", "Price must be greater than 0"))
        except (InvalidOperation, ValueError):
            row_errors.append(RowError(row_num, "price", "Invalid price value"))

        # Timestamp
        try:
            pd.Timestamp(row.get("timestamp"))
        except (ValueError, TypeError):
            row_errors.append(RowError(row_num, "timestamp", "Invalid timestamp format"))

        if row_errors:
            result.errors.extend(row_errors)
        else:
            result.valid_rows.append(
                {
                    "transaction_id": tx_id,
                    "client_id": client_id,
                    "isin": isin,
                    "action": action,
                    "quantity": Decimal(str(row["quantity"])),
                    "price": Decimal(str(row["price"])),
                    "timestamp": pd.Timestamp(row["timestamp"]),
                }
            )

    return result
