---
globs: backend/**/*.py
---

# Python Style

- Format with Ruff. Follow existing pyproject.toml config.
- Use `Decimal` for all monetary/financial values — never `float`.
- Use `StrEnum` for string enumerations (see `app/constants.py`).
- Use `X | None` union syntax, not `Optional[X]`.
- Use `dict[str, Any]` lowercase generics, not `Dict[str, Any]`.
- Imports: stdlib -> third-party -> local, separated by blank lines.
- No magic numbers. Reference constants from `app/constants.py`.
- Type-hint all function signatures (params + return).
- Use `from __future__ import annotations` only if needed for forward refs.
