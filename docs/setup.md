# Setup Guide

## Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.11+ with [uv](https://docs.astral.sh/uv/) (for local backend development)

## Docker Quickstart

```bash
# Clone and start everything
git clone <repo-url> && cd ibi-fullstack-finops-dashboard
docker-compose up --build
```

Services will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432 (user: `finops`, password: `finops`, db: `finops_db`)

Startup order is enforced via health checks: PostgreSQL → Backend (runs migrations) → Frontend.

## Local Backend Development

```bash
cd backend

# Install dependencies
uv sync

# Set environment variables (or create .env file)
export DATABASE_URL=postgresql://finops:finops@localhost:5432/finops_db

# Run migrations
uv run alembic upgrade head

# Start the server
uv run uvicorn app.main:app --reload --port 8000

# Run tests (uses SQLite, no PostgreSQL needed)
uv run pytest -v
```

## Local Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Set API URL
export NEXT_PUBLIC_API_URL=http://localhost:8000

# Start dev server
npm run dev
```

Frontend will be available at http://localhost:3000.

## Environment Variables

### Backend

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | — | PostgreSQL connection string |
| `LLM_PROVIDER` | `mock` | LLM provider: `anthropic`, `openai`, or `mock` |
| `LLM_MODEL` | — | Model name (e.g., `claude-sonnet-4-20250514`) |
| `LLM_TEMPERATURE` | `0.7` | LLM temperature |
| `LLM_MAX_TOKENS` | `1024` | Max tokens for LLM response |
| `ANTHROPIC_API_KEY` | — | Anthropic API key (if using anthropic provider) |
| `OPENAI_API_KEY` | — | OpenAI API key (if using openai provider) |
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Allowed CORS origins (JSON array) |
| `LOG_LEVEL` | `INFO` | Python logging level |

### Frontend

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend API base URL |

## Seeding Sample Data

After the stack is running:

```bash
curl -X POST http://localhost:8000/api/v1/transactions/upload \
  -F "file=@sample_data/transactions_sample.csv"
```

This uploads 6 sample transactions for 3 clients, triggering portfolio calculation and violation detection.

## Troubleshooting

### Port conflicts

If ports 3000, 5432, or 8000 are in use, stop the conflicting services or modify `docker-compose.yml` port mappings.

### Database connection errors

Ensure PostgreSQL is running and accessible. For Docker, check `docker-compose ps` for health status. For local dev, verify the `DATABASE_URL` matches your PostgreSQL instance.

### Frontend can't reach backend

Verify `NEXT_PUBLIC_API_URL` is set correctly. In Docker, the frontend container connects via `http://localhost:8000` (host network). For local dev, ensure the backend is running on port 8000 with CORS enabled.

### Tests fail with import errors

Ensure you're running tests from the `backend/` directory with `uv run pytest`, which activates the correct virtual environment and Python path.

### Migration errors

If the database schema is out of sync: drop the database, recreate it, and re-run migrations. See the `db-reset` Claude command.
