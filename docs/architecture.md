# Architecture

## System Overview

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Next.js    │────▶│   FastAPI        │────▶│  PostgreSQL  │
│   Frontend   │◀────│   Backend        │◀────│  Database    │
│  :3000       │     │  :8000           │     │  :5432       │
└─────────────┘     └────────┬──────────┘     └──────────────┘
                             │
                    ┌────────▼──────────┐
                    │  LLM Provider     │
                    │  (Anthropic /     │
                    │   OpenAI / Mock)  │
                    └───────────────────┘
```

All three services are orchestrated via `docker-compose.yml` with health-check-based startup ordering.

## Backend Architecture

### Layered Design

```
Route Handlers (api/v1/)     ← Thin controllers, return ApiResponse[T]
        │
Service Layer (services/)    ← Business logic, DB operations
        │
   ┌────┴─────┐
   │          │
Models    Utilities          ← ORM models + pure functions
(models/) (utils/)
```

### Upload Pipeline

The core workflow triggered by `POST /api/v1/transactions/upload`:

```
CSV/XLSX File
    │
    ▼
┌─────────────────┐
│  csv_parser.py   │  Parse file via pandas, normalize headers
└────────┬────────┘
         ▼
┌─────────────────┐
│ validation_svc   │  Row-level + batch-level checks
└────────┬────────┘
         ▼
┌─────────────────┐
│ upload_service   │  Persist valid rows, upsert clients, assign batch_id
└────────┬────────┘
         ▼
┌─────────────────┐
│ portfolio_svc    │  FIFO recalculation per affected client/ISIN
└────────┬────────┘
         ▼
┌─────────────────┐
│ violation_svc    │  Detect short selling, concentration, day trading
└─────────────────┘
```

### FIFO Engine (`utils/fifo_engine.py`)

Pure function with zero side effects. Takes a list of chronologically sorted transactions for a single client+ISIN pair.

- Uses `collections.deque` for lot tracking
- Buys append to queue; sells consume from front (FIFO)
- Tracks realized P&L per consumed lot
- Detects short sells (sell quantity exceeds available lots)
- Returns `FIFOResult`: lots, realized_pnl, current_quantity, average_cost, total_invested, short_sells

### LLM Factory (`services/llm/`)

```
factory.py ─── create_llm_provider(settings)
                    │
           ┌────────┼────────┐
           ▼        ▼        ▼
      Anthropic   OpenAI    Mock
      Provider    Provider  Provider
```

- `LLMProvider` abstract base class with `generate_insights(prompt)` method
- Factory reads `LLM_PROVIDER` from config
- Insight service catches provider exceptions and falls back to `MockProvider`
- Mock returns deterministic results for testing and demo

### Exception Hierarchy

```
AppException (base: 500)
├── UploadError (400)
├── ValidationError (422)
└── NotFoundError (404)
```

Global handlers in `exceptions.py` convert exceptions to the `ApiResponse` envelope with `success: false`.

### Response Envelope

Every endpoint returns:

```json
{
  "success": true,
  "data": "<payload>",
  "error": null,
  "pagination": {
    "page": 1,
    "page_size": 50,
    "total_items": 200,
    "total_pages": 4
  }
}
```

Defined in `schemas/base.py` as `ApiResponse[T]` generic.

## Frontend Architecture

### App Router Structure

```
src/app/
├── layout.tsx              Root layout (dark theme, fonts, AppShell)
├── page.tsx                Home → redirects to upload
├── upload/page.tsx         File upload with drag-and-drop
└── clients/
    ├── page.tsx            Client list with search + sort
    └── [clientId]/
        ├── layout.tsx      Tabbed navigation (portfolio | actions)
        ├── portfolio/      FIFO holdings + summary cards
        └── actions/        Violations + AI insights
```

### State Management

- **Server state**: TanStack Query v5 — cached, auto-refetched, invalidated on mutations
- **Ephemeral state**: React Context for toast notifications (auto-dismiss 5s)
- **No client-side global store** — all data flows from the API

### API Client Layer

```
types/           TypeScript interfaces (mirror Pydantic schemas)
    ↓
lib/api/         Typed fetch functions per resource
    ↓
lib/hooks/       TanStack Query hooks (useQuery / useMutation)
    ↓
components/      Consume hooks, render UI
```

### UI Component Organization

```
components/
├── layout/      Sidebar, TopBar, PageHeader
├── upload/      FileDropZone, ValidationSummary, ErrorTable
├── clients/     ClientsTable
├── portfolio/   PortfolioSummaryCards, HoldingsTable
├── actions/     ViolationsList, InsightsPanel
└── ui/          Card, Badge, Spinner, Skeleton, EmptyState, ProgressBar
```
