"""Violation ORM model."""

from datetime import datetime

from sqlalchemy import JSON, CheckConstraint, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.base import Base


class Violation(Base):
    __tablename__ = "violations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("clients.client_id"), nullable=False
    )
    transaction_id: Mapped[str | None] = mapped_column(
        String(50), ForeignKey("transactions.transaction_id"), nullable=True
    )
    violation_type: Mapped[str] = mapped_column(String(30), nullable=False)
    severity: Mapped[str] = mapped_column(String(10), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    client = relationship("Client", back_populates="violations")

    __table_args__ = (
        CheckConstraint(
            "violation_type IN ('short_selling', 'concentration_risk', 'day_trading')",
            name="ck_viol_type",
        ),
        CheckConstraint("severity IN ('error', 'warning')", name="ck_viol_severity"),
        Index("ix_viol_client_type", "client_id", "violation_type"),
    )
