Run all linters and type checks across the project.

Steps:
1. Backend — Ruff linting:
   ```
   cd backend && uv run ruff check .
   ```
2. Backend — Ruff formatting:
   ```
   cd backend && uv run ruff format --check .
   ```
3. Frontend — ESLint:
   ```
   cd frontend && npm run lint
   ```
4. Frontend — TypeScript type checking:
   ```
   cd frontend && npx tsc --noEmit
   ```
5. Report results for each tool: pass or list of issues.
6. If there are auto-fixable issues, offer to run `ruff check --fix` or `ruff format`.
