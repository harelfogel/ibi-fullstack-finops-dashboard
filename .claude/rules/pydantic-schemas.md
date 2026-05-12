---
globs: backend/app/schemas/**/*.py
---

# Pydantic Schema Conventions

- Use Pydantic v2 with `model_config = {"from_attributes": True}` for ORM conversion.
- All API responses wrap in `ApiResponse[T]` from `app/schemas/base.py`.
- Use `Field()` for constraints: `ge=`, `le=`, `min_length=`, `max_length=`.
- Use `X | None = None` for optional fields, not `Optional[X]`.
- Decimal fields stay as `Decimal` — do not convert to float.
- Separate schemas for input vs. output when they differ.
- Use `Generic[T]` only in base envelope; concrete schemas use concrete types.
- Keep schemas in files matching the model they represent (e.g., `schemas/client.py`).
