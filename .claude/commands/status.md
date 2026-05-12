Show a compact project status dashboard.

Gather and display:

1. **Git**: Current branch, uncommitted changes count, last commit message.
2. **Docker**: Running containers and their health status (`docker-compose ps`).
3. **Tests**: Run `cd backend && uv run pytest -q` and report pass/fail summary.
4. **Frontend Build**: Run `cd frontend && npx tsc --noEmit` and report success/error count.
5. **Alembic**: Current migration head (`cd backend && uv run alembic current`).
6. **Database**: Table row counts if PostgreSQL is running:
   ```
   docker-compose exec postgres psql -U finops -d finops_db -c "SELECT 'clients', count(*) FROM clients UNION ALL SELECT 'transactions', count(*) FROM transactions UNION ALL SELECT 'portfolio_positions', count(*) FROM portfolio_positions UNION ALL SELECT 'violations', count(*) FROM violations;"
   ```

Format as a clean dashboard with section headers.
