# Architecture & SOLID Principles

## Single Responsibility (S)
- Each service handles one domain concern: `fifo_engine.py` (FIFO math), `violation_service.py` (compliance), `insight_service.py` (AI).
- Routes are thin controllers — delegate all logic to services.
- Frontend: one hook per resource, one component per feature area.

## Open/Closed (O)
- LLM factory pattern: add new providers (e.g., Gemini) without modifying existing code.
- Violation detection: each rule is an independent function, new rules added alongside existing ones.
- API response envelope (`ApiResponse[T]`) is generic — works for any data type.

## Liskov Substitution (L)
- All `LLMProvider` subclasses (Anthropic, OpenAI, Mock) are fully interchangeable.
- All implement `generate_insights(prompt, system_prompt) -> InsightResponse` identically.
- Mock provider returns valid `InsightResponse` — callers cannot distinguish from real provider.

## Interface Segregation (I)
- Services expose minimal, focused methods — no god classes.
- `LLMProvider` has one method: `generate_insights()`.
- DB models define only the columns and relationships they own.

## Dependency Injection (D)
- FastAPI `Depends(get_db)` injects database sessions into routes.
- LLM provider created via factory, not hardcoded in services.
- Tests swap PostgreSQL for SQLite via fixture override — zero code changes.
- Settings loaded from environment, not hardcoded values.

## Layered Architecture
```
Routes (thin controllers)
  -> Services (business logic)
    -> Models (data access)
    -> Utils (pure functions, no side effects)
```
- Routes never access DB directly — always through services.
- Utils (`fifo_engine.py`, `csv_parser.py`) are pure functions with no DB dependencies.
- Services coordinate between models, utils, and external providers.

## Frontend Architecture
- `app/` — Next.js pages and layouts (routing layer).
- `components/` — React components organized by feature.
- `lib/api/` — Typed API client functions (data access layer).
- `lib/hooks/` — TanStack Query hooks (state management layer).
- `lib/providers/` — Context providers (cross-cutting concerns).
- `types/` — TypeScript interfaces mirroring backend schemas.
