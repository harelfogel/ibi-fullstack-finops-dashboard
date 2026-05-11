"""Initial schema with all tables.

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── clients ─────────────────────────────────────────────────
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("client_id", sa.String(50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_clients_client_id", "clients", ["client_id"], unique=True)

    # ── transactions ────────────────────────────────────────────
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("transaction_id", sa.String(50), nullable=False),
        sa.Column("client_id", sa.String(50), nullable=False),
        sa.Column("isin", sa.String(12), nullable=False),
        sa.Column("action", sa.String(4), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 6), nullable=False),
        sa.Column("price", sa.Numeric(18, 6), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("upload_batch_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("action IN ('buy', 'sell')", name="ck_tx_action"),
        sa.CheckConstraint("quantity > 0", name="ck_tx_quantity_positive"),
        sa.CheckConstraint("price > 0", name="ck_tx_price_positive"),
        sa.ForeignKeyConstraint(["client_id"], ["clients.client_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tx_transaction_id", "transactions", ["transaction_id"], unique=True)
    op.create_index("ix_tx_client_isin", "transactions", ["client_id", "isin"])
    op.create_index("ix_tx_client_timestamp", "transactions", ["client_id", "timestamp"])
    op.create_index("ix_tx_batch", "transactions", ["upload_batch_id"])

    # ── portfolio_positions ─────────────────────────────────────
    op.create_table(
        "portfolio_positions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("client_id", sa.String(50), nullable=False),
        sa.Column("isin", sa.String(12), nullable=False),
        sa.Column("current_quantity", sa.Numeric(18, 6), server_default="0", nullable=False),
        sa.Column("average_cost", sa.Numeric(18, 6), server_default="0", nullable=False),
        sa.Column("total_invested", sa.Numeric(18, 6), server_default="0", nullable=False),
        sa.Column("realized_pnl", sa.Numeric(18, 6), server_default="0", nullable=False),
        sa.Column("unrealized_pnl", sa.Numeric(18, 6), server_default="0", nullable=False),
        sa.Column("market_value", sa.Numeric(18, 6), server_default="0", nullable=False),
        sa.Column("last_calculated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["clients.client_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_pos_client_isin", "portfolio_positions", ["client_id", "isin"], unique=True
    )

    # ── violations ──────────────────────────────────────────────
    op.create_table(
        "violations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("client_id", sa.String(50), nullable=False),
        sa.Column("transaction_id", sa.String(50), nullable=True),
        sa.Column("violation_type", sa.String(30), nullable=False),
        sa.Column("severity", sa.String(10), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column(
            "detected_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "violation_type IN ('short_selling', 'concentration_risk', 'day_trading')",
            name="ck_viol_type",
        ),
        sa.CheckConstraint("severity IN ('error', 'warning')", name="ck_viol_severity"),
        sa.ForeignKeyConstraint(["client_id"], ["clients.client_id"]),
        sa.ForeignKeyConstraint(["transaction_id"], ["transactions.transaction_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_viol_client_type", "violations", ["client_id", "violation_type"])


def downgrade() -> None:
    op.drop_table("violations")
    op.drop_table("portfolio_positions")
    op.drop_table("transactions")
    op.drop_table("clients")
