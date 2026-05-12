# Git Conventions

- Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`.
- Keep commit messages concise — subject line under 72 characters.
- Never commit `.env` files or API keys. Use `.env.example` for templates.
- One logical change per commit — don't mix features with unrelated refactors.
- Run tests before committing: `cd backend && uv run pytest -v`.
- Run linters before committing: `ruff check .` and `npm run lint`.
