"""Transaction ORM model."""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transaction_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    client_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("clients.client_id"), nullable=False
    )
    isin: Mapped[str] = mapped_column(String(12), nullable=False)
    action: Mapped[str] = mapped_column(String(4), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    upload_batch_id: Mapped[uuid.UUID] = mapped_column(Uuid(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    client = relationship("Client", back_populates="transactions")

    __table_args__ = (
        CheckConstraint("action IN ('buy', 'sell')", name="ck_tx_action"),
        CheckConstraint("quantity > 0", name="ck_tx_quantity_positive"),
        CheckConstraint("price > 0", name="ck_tx_price_positive"),
        Index("ix_tx_transaction_id", "transaction_id", unique=True),
        Index("ix_tx_client_isin", "client_id", "isin"),
        Index("ix_tx_client_timestamp", "client_id", "timestamp"),
        Index("ix_tx_batch", "upload_batch_id"),
    )
