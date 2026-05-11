"""Upload orchestrator service: parse → validate → persist → recalculate."""

import uuid
from datetime import timezone

from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.transaction import Transaction
from app.services.portfolio_service import recalculate_portfolio
from app.services.validation_service import ValidationResult, validate_transactions
from app.services.violation_service import detect_violations
from app.utils.csv_parser import parse_upload_file


def process_upload(filename: str, content: bytes, db: Session) -> dict:
    """Process a file upload end-to-end.

    Steps:
    1. Parse the file (CSV/XLSX)
    2. Validate all rows
    3. Persist valid transactions (with batch ID)
    4. Upsert clients
    5. Recalculate portfolio positions (FIFO)
    6. Detect violations

    Args:
        filename: Original filename.
        content: Raw file bytes.
        db: Database session.

    Returns:
        Dict with upload summary including batch_id, row counts, and errors.
    """
    # 1. Parse
    df = parse_upload_file(filename, content)

    # 2. Validate
    validation: ValidationResult = validate_transactions(df, db)

    batch_id = uuid.uuid4()
    affected_clients: set[str] = set()

    # 3. Persist valid transactions
    for row in validation.valid_rows:
        client_id = row["client_id"]
        affected_clients.add(client_id)

        # Upsert client
        existing_client = (
            db.query(Client).filter(Client.client_id == client_id).first()
        )
        if not existing_client:
            db.add(Client(client_id=client_id))
            db.flush()

        # Make timestamp timezone-aware
        ts = row["timestamp"]
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)

        # Create transaction
        db.add(
            Transaction(
                transaction_id=row["transaction_id"],
                client_id=client_id,
                isin=row["isin"],
                action=row["action"],
                quantity=row["quantity"],
                price=row["price"],
                timestamp=ts,
                upload_batch_id=batch_id,
            )
        )

    db.flush()

    # 4-5. Recalculate portfolio and detect violations for affected clients
    for client_id in affected_clients:
        recalculate_portfolio(client_id, db)
        detect_violations(client_id, db)

    db.commit()

    return {
        "batch_id": str(batch_id),
        "total_rows": validation.total_rows,
        "valid_rows": len(validation.valid_rows),
        "error_rows": len(validation.errors),
        "errors": [
            {"row": e.row, "field": e.field, "message": e.message}
            for e in validation.errors
        ],
        "affected_clients": sorted(affected_clients),
    }
