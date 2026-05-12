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
