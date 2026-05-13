# IBI FinOps Dashboard

Fullstack financial operations dashboard for transaction processing, portfolio management (FIFO P&L), rule violation detection, and AI-generated portfolio insights.

## Tech Stack

| Layer    | Technology                                                         |
| -------- | ------------------------------------------------------------------ |
| Backend  | Python 3.11, FastAPI, SQLAlchemy 2.0, Alembic, pandas, Pydantic v2 |
| Database | PostgreSQL 16                                                      |
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS                  |
| State    | TanStack Query v5, React Context                                   |
| AI       | Anthropic Claude API (with mock fallback)                          |
| Infra    | Docker, docker-compose                                             |
| Testing  | pytest (31 tests)                                                  |

## Quick Start

### Docker (recommended)

```bash
docker-compose up --build
```

Services:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

### Local Development

**Backend:**

```bash
cd backend
uv sync
cp .env.example .env
# Start PostgreSQL, then:
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000
```

> **AI Insights:** Locally, AI insights use a mock provider by default (no API key needed). To enable real Anthropic Claude analysis, set `LLM_PROVIDER=anthropic` and add your `ANTHROPIC_API_KEY` in `backend/.env`.

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

**Run tests:**

```bash
cd backend
uv run pytest -v
```

## Architecture

### Backend

```
backend/app/
├── main.py              # FastAPI app, CORS, routers
├── config.py            # Pydantic settings from env
├── constants.py         # Enums, thresholds, error codes
├── exceptions.py        # Custom exceptions + handlers
├── api/v1/              # Route handlers
├── schemas/             # Pydantic DTOs
├── models/              # SQLAlchemy ORM
├── services/            # Business logic layer
│   ├── upload_service    # Orchestrator: parse -> validate -> persist -> calculate
│   ├── validation_service # Row + batch validation
│   ├── portfolio_service  # FIFO P&L calculation
│   ├── violation_service  # Rule detection
│   └── insight_service    # AI insights + mock fallback
└── utils/
    ├── csv_parser        # pandas CSV/XLSX parser
    └── fifo_engine       # Pure FIFO lot tracking
```

### Frontend

```
frontend/src/
├── app/                 # Next.js App Router pages
│   ├── upload/          # File upload with validation
│   ├── clients/         # Client overview table
│   └── clients/[id]/    # Portfolio + Actions tabs
├── components/          # UI, layout, feature components
├── lib/                 # API client, hooks, providers
└── types/               # TypeScript interfaces
```

### API Endpoints

| Method | Path                              | Description                   |
| ------ | --------------------------------- | ----------------------------- |
| GET    | `/health`                         | Health check                  |
| POST   | `/api/v1/transactions/upload`     | Upload CSV/XLSX               |
| GET    | `/api/v1/transactions`            | List transactions (paginated) |
| GET    | `/api/v1/clients`                 | List clients with summaries   |
| GET    | `/api/v1/clients/{id}/portfolio`  | FIFO portfolio positions      |
| GET    | `/api/v1/clients/{id}/violations` | Rule violations               |
| GET    | `/api/v1/clients/{id}/insights`   | AI portfolio analysis         |

### Key Design Decisions

- **FIFO Engine**: Pure function with deque-based lot tracking - no side effects, fully testable
- **Zero Magic Numbers**: All thresholds, limits, and codes defined in `constants.py`
- **Response Envelope**: Consistent `{ success, data, error, pagination }` across all endpoints
- **AI Fallback**: Real Anthropic Claude API in production; deterministic mock insights locally (no API key needed) or on failure
- **Violation Detection**: Short selling (error), concentration risk (warning), day trading (warning)

## Assumptions

- Uploaded CSV/XLSX transaction files are the source of truth for client activity.
- Each transaction has a unique `TransactionId`; duplicate uploads are rejected.
- Supported transaction actions are `buy` and `sell`.
- Quantities and prices must be positive values.
- ISIN values are expected to be 12 characters.
- Portfolio positions are recalculated from transaction history after each upload.
- FIFO is used for realized P&L and remaining lot cost basis.
- Current market value uses the latest transaction price for each ISIN as a market-price proxy.
- Supported rule checks are short selling, concentration risk, and day trading.
- Concentration risk is flagged when one ISIN represents more than 50% of a client's portfolio value.
- Day trading is flagged when there are 3 or more buy/sell pairs for the same ISIN inside a 24-hour window.
- AI insights use Anthropic Claude when configured; local/demo runs can use the deterministic mock fallback.

## Database and Seed Data

- Database schema is managed with Alembic migrations in `backend/alembic/versions/`.
- The main schema migration is `backend/alembic/versions/001_initial_schema.py`.
- Seed/sample input data is provided in the `sample_data/` folder.
- `sample_data/transactions_sample.csv` is the primary seed file for a normal demo upload.
- The `sample_data/` folder also includes QA datasets for validation errors, short selling, day trading, multi-lot FIFO, full-sell/loss handling, concentration risk, duplicate uploads, sells-only, and buys-only scenarios.

After starting the stack, seed the database by uploading a CSV through the UI or with:

```bash
curl -X POST http://localhost:8000/api/v1/transactions/upload \
  -F "file=@sample_data/transactions_sample.csv"
```

## Testing

31 tests covering:

- FIFO engine: single buy, partial sell, multi-lot FIFO order, short sell detection, loss scenarios
- Validation: quantity/price/action/ISIN validation, duplicate detection
- Violations: short selling, concentration risk, day trading pattern detection
- Portfolio: position calculation, multi-ISIN, summary aggregation
- Upload E2E: full upload flow, duplicate rejection, client/portfolio creation

## Repository Layout

This project is organized as a monorepo:

- `backend/` - FastAPI API, SQLAlchemy models, Alembic migrations, tests
- `frontend/` - Next.js dashboard, typed API client, UI components
- `docs/` - setup, architecture, database, API, and testing notes
- `sample_data/` - CSV fixtures for upload and QA scenarios
