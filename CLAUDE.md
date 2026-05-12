# IBI FinOps Dashboard

## Project Overview

Home assignment for Mid Fullstack Developer position at IBI. Financial operations dashboard: CSV upload of stock transactions, FIFO-based portfolio calculation, compliance violation detection, AI-generated insights.

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend | Python + FastAPI | 3.11 / 0.111 |
| ORM | SQLAlchemy | 2.0 (Mapped[] style) |
| Schemas | Pydantic | v2 (from_attributes) |
| Migrations | Alembic | Latest |
| Database | PostgreSQL | 16 (SQLite for tests) |
| Frontend | Next.js (App Router) | 14 |
| Language | TypeScript | Strict mode |
| Styling | Tailwind CSS | 3.4 |
| Server State | TanStack Query | v5 |
| AI | Anthropic / OpenAI / Mock | Factory pattern |
| Containers | Docker + Compose | Multi-stage builds |

## Directory Layout

```
backend/
  app/
    api/v1/          # Route handlers (thin controllers)
    models/          # SQLAlchemy ORM models
    schemas/         # Pydantic v2 DTOs
    services/        # Business logic layer
    services/llm/    # LLM provider factory + implementations
    utils/           # Pure utilities (fifo_engine, csv_parser)
    db/              # Engine + session factory
    config.py        # Pydantic BaseSettings (env vars)
    constants.py     # Enums, thresholds, zero magic numbers
    exceptions.py    # AppException hierarchy + handlers
    dependencies.py  # FastAPI Depends() callables
  tests/             # pytest (SQLite fixtures, factories)
  alembic/           # Database migrations

frontend/
  src/
    app/             # Next.js App Router pages
    components/      # React components by feature
    lib/api/         # Typed fetch wrapper per resource
    lib/hooks/       # TanStack Query hooks
    lib/providers/   # QueryProvider, ToastProvider
    lib/utils/       # cn(), format helpers, constants
    types/           # TypeScript interfaces (mirror backend schemas)
```

## Architecture Patterns

- **Response envelope**: All endpoints return `ApiResponse<T>` with `success`, `data`, `error`, `pagination`
- **Exception hierarchy**: `AppException` base -> `UploadError(400)`, `ValidationError(422)`, `NotFoundError(404)`
- **Service layer**: Routes are thin; business logic lives in `services/`
- **FIFO engine**: Pure function in `utils/fifo_engine.py` — no DB side effects, deque-based lot tracking
- **LLM factory**: `create_llm_provider()` returns Anthropic/OpenAI/Mock; insight service falls back to Mock on failure
- **Upload pipeline**: Parse CSV -> Validate rows -> Persist transactions -> Recalculate portfolio (FIFO) -> Detect violations
- **Violation detection**: Short selling (ERROR), concentration risk >50% (WARNING), day trading >=3 pairs/24h (WARNING)

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Health check |
| POST | `/api/v1/transactions/upload` | Upload CSV/XLSX file |
| GET | `/api/v1/transactions` | List transactions (paginated, filterable) |
| GET | `/api/v1/clients` | List all clients with summaries |
| GET | `/api/v1/clients/{client_id}` | Client detail |
| GET | `/api/v1/clients/{client_id}/portfolio` | FIFO portfolio positions |
| GET | `/api/v1/clients/{client_id}/violations` | Compliance violations |
| GET | `/api/v1/clients/{client_id}/insights` | AI-generated insights |

## Database Tables

| Table | Key Columns | Notes |
|-------|-------------|-------|
| `clients` | `client_id` (unique) | Auto-created on upload |
| `transactions` | `transaction_id` (unique), `client_id` FK, `isin`, `action`, `quantity`, `price` | Numeric(18,6), CHECK constraints |
| `portfolio_positions` | `client_id` + `isin` (unique together) | FIFO-calculated, `realized_pnl`, `unrealized_pnl` |
| `violations` | `client_id` FK, `violation_type`, `severity` | JSON details column |

## Dev Commands

```bash
# Docker (full stack)
docker-compose up --build

# Backend local
cd backend && uv run uvicorn app.main:app --reload --port 8000

# Tests
cd backend && uv run pytest -v

# Frontend local
cd frontend && npm run dev

# Lint
cd backend && uv run ruff check . && uv run ruff format --check .
cd frontend && npm run lint && npx tsc --noEmit

# Migrations
cd backend && uv run alembic upgrade head
```

## Conventions

- **Zero magic numbers**: All thresholds/limits in `constants.py` with named constants and enums
- **Type unions**: Use `X | None` syntax (not `Optional[X]`)
- **Decimal precision**: All monetary values use `Decimal` and `Numeric(18,6)`
- **Backend naming**: snake_case everywhere, Ruff-formatted
- **Frontend naming**: camelCase for variables, PascalCase for components, named exports
- **Commits**: Conventional commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`)
- **Environment**: Never commit `.env`; use `.env.example` for templates
