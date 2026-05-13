---
globs: backend/app/models/**/*.py
---

# SQLAlchemy Model Conventions

- Use SQLAlchemy 2.0 `Mapped[]` annotation style with `mapped_column()`.
- Inherit from `Base` (DeclarativeBase) in `app/models/base.py`.
- Use `TimestampMixin` for `created_at` / `updated_at` columns.
- Monetary columns: `Numeric(18, 6)` — never Float.
- Add `CheckConstraint` for domain rules (e.g., `quantity > 0`, `action IN ('buy','sell')`).
- Add indexes on frequently queried columns (client_id, isin, composite).
- Foreign keys reference the `id` column or natural key as appropriate.
- JSON columns use `JSON` type (not JSONB) for SQLite test compatibility.
- Define `__tablename__` explicitly on every model.
- Relationships use `relationship()` with `back_populates`.

## Data Integrity & ACID Compliance
- Use explicit foreign key constraints — enforce referential integrity at the DB level.
- Wrap related writes in a single `session.commit()` — e.g., upload persists transactions + recalculates portfolio + detects violations atomically.
- Use `session.flush()` before dependent queries to ensure write visibility within a transaction.
- CheckConstraints enforce domain invariants at the DB level (`quantity > 0`, `price > 0`).
- Unique constraints prevent duplicate records: `transaction_id`, `client_id + isin` composite.

## Indexing Strategy
- Index all foreign key columns: `client_id` on transactions, portfolio_positions, violations.
- Composite index on `(client_id, isin)` for portfolio position lookups.
- Index `transaction_id` for uniqueness checks during upload.
- Add indexes on columns used in WHERE/ORDER BY: `created_at`, `violation_type`.
