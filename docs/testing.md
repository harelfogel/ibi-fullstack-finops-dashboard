# Testing

## Overview

- **Framework**: pytest
- **Database**: SQLite (in-memory, per-test isolation)
- **Test count**: 31 passing tests
- **Test lines**: ~700 lines

## Test Architecture

```
tests/
├── conftest.py                  # Fixtures: db, client (TestClient)
├── factories.py                 # make_tx() helper, SAMPLE_CSV_CONTENT
├── test_fifo_engine.py          # 8 tests — pure function, no DB
├── test_validation_service.py   # 8 tests — row/batch validation
├── test_violation_service.py    # 5 tests — rule detection
├── test_portfolio_service.py    # 4 tests — FIFO P&L calculation
└── test_upload_endpoint.py      # 6 tests — E2E HTTP upload flow
```

## Fixtures

### `db` (function scope)

Fresh SQLite database per test. Creates all tables via `Base.metadata.create_all()`, yields a session, then drops all tables on teardown.

### `client` (function scope)

FastAPI `TestClient` with the DB dependency overridden to use the test database. Cleared after each test.

### `make_tx()` factory

Creates `TransactionInput` objects with minimal required fields:

```python
make_tx(tx_id="TX001", action="buy", quantity=100, price=50.0)
```

### `SAMPLE_CSV_CONTENT`

A 6-row CSV string with valid transactions for clients C001, C002, C003. Used for upload E2E tests.

## Coverage by Module

| Module | Tests | What's Covered |
|--------|-------|----------------|
| `fifo_engine.py` | 8 | Single buy, partial sell, full sell, multi-lot FIFO order, short sell detection, loss scenarios, empty input |
| `validation_service.py` | 8 | Missing fields, invalid quantity/price/action, ISIN format, duplicate transaction IDs, batch + DB duplicate detection |
| `violation_service.py` | 5 | Short selling detection, concentration risk threshold, day trading pattern, no-violation baseline, multi-violation client |
| `portfolio_service.py` | 4 | Single position calculation, multi-ISIN portfolio, summary aggregation, client not found error |
| Upload endpoint | 6 | Full upload flow, duplicate handling, invalid file format, missing columns, downstream effects (portfolio + violations created) |

## Writing New Tests

### Pattern: AAA (Arrange, Act, Assert)

```python
def test_fifo_partial_sell(self):
    # Arrange
    txs = [
        make_tx("TX1", "buy", 100, 50.0),
        make_tx("TX2", "sell", 30, 60.0),
    ]

    # Act
    result = calculate_fifo(txs)

    # Assert
    assert result.current_quantity == 70
    assert result.realized_pnl == Decimal("300.00")
```

### Guidelines

- Test naming: `test_{unit}_{scenario}` (e.g., `test_fifo_short_sell_detection`)
- Assert specific values, not just truthiness
- Test both happy paths and error cases
- For service tests, create DB records directly via the session
- For E2E tests, use the `client` fixture and make HTTP requests
- Keep tests independent — no shared mutable state between tests
- Use `Decimal` for financial assertions to avoid float comparison issues

### Running Tests

```bash
# All tests
cd backend && uv run pytest -v

# Specific file
cd backend && uv run pytest -v tests/test_fifo_engine.py

# Specific test
cd backend && uv run pytest -v tests/test_fifo_engine.py::TestFIFOEngine::test_fifo_single_buy

# With coverage
cd backend && uv run pytest --cov=app --cov-report=term-missing
```
