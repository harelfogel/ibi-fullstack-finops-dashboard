---
globs: "{docker-compose.yml,**/Dockerfile}"
---

# Docker Conventions

- Backend Dockerfile: multi-stage build with `uv` for dependency management.
- Frontend Dockerfile: multi-stage build (deps -> build -> runner), standalone Next.js output.
- Frontend runner uses non-root `nextjs` user.
- docker-compose.yml service order: postgres -> backend -> frontend.
- Health checks: postgres uses `pg_isready`, backend uses `/health` endpoint.
- `depends_on` with `condition: service_healthy` for startup ordering.
- PostgreSQL credentials: `finops:finops@postgres:5432/finops_db`.
- Backend runs Alembic migrations on startup before uvicorn.
- Environment variables passed via docker-compose `environment` block.
- `postgres_data` named volume for database persistence.
