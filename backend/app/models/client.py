"""Client ORM model."""

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Client(Base, TimestampMixin):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Relationships
    transactions = relationship("Transaction", back_populates="client", lazy="selectin")
    positions = relationship("PortfolioPosition", back_populates="client", lazy="selectin")
    violations = relationship("Violation", back_populates="client", lazy="selectin")

    __table_args__ = (Index("ix_clients_client_id", "client_id", unique=True),)
