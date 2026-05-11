"""Test data factories."""

from decimal import Decimal

from app.utils.fifo_engine import TransactionInput


def make_tx(
    tx_id: str = "T001",
    action: str = "buy",
    quantity: str | Decimal = "100",
    price: str | Decimal = "50.00",
) -> TransactionInput:
    """Create a TransactionInput for FIFO testing."""
    return TransactionInput(
        transaction_id=tx_id,
        action=action,
        quantity=Decimal(str(quantity)),
        price=Decimal(str(price)),
    )


SAMPLE_CSV_CONTENT = (
    b"ClientId,TransactionId,ISIN,Action,Quantity,Price,Timestamp\n"
    b"C001,T1001,US1234567890,buy,50,100.5,2023-11-01T10:00:00\n"
    b"C001,T1002,US1234567890,sell,20,105.2,2023-11-05T11:00:00\n"
    b"C002,T2001,US0987654321,buy,100,80,2023-11-03T09:00:00\n"
    b"C001,T1003,US9999999999,buy,10,98,2023-11-06T15:00:00\n"
    b"C002,T2002,US0987654321,sell,50,85,2023-11-07T10:30:00\n"
    b"C003,T3001,US1111111111,buy,200,50,2023-11-02T12:00:00\n"
)
