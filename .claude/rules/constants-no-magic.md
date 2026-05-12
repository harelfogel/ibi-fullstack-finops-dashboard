---
globs: backend/**/*.py
---

# No Magic Numbers

- All thresholds, limits, and configuration values live in `app/constants.py`.
- Reference named constants: `MAX_UPLOAD_SIZE_BYTES`, `CONCENTRATION_RISK_THRESHOLD`, etc.
- Use `StrEnum` classes for categorical values: `TransactionAction`, `ViolationType`, `ViolationSeverity`, `LLMProviderType`, `ErrorCode`.
- Use `EXPECTED_CSV_COLUMNS` dict for CSV header normalization.
- Never hardcode numeric thresholds, string literals for enums, or column names inline.
- If a new constant is needed, add it to `constants.py` with a descriptive name and comment.
