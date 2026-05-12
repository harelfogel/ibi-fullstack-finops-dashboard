---
globs: backend/tests/**/*.py
---

# Testing Conventions

- Tests use SQLite via fixtures in `conftest.py` — fresh DB per test function.
- Use `make_tx()` factory from `tests/factories.py` for `TransactionInput` objects.
- Use `SAMPLE_CSV_CONTENT` from `tests/factories.py` for upload E2E tests.
- Follow AAA pattern: Arrange, Act, Assert — separated by blank lines.
- Test naming: `test_<unit>_<scenario>` (e.g., `test_fifo_single_buy`).
- FIFO engine tests: pure function, no DB needed.
- Service tests: use `db` fixture, create records directly.
- E2E tests: use `client` fixture (TestClient with DB override).
- Assert specific values, not just truthiness. Check counts, amounts, types.
- Test both happy path and error cases for each feature.
