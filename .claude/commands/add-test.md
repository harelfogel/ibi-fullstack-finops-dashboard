Generate tests for a specified module.

Usage: Provide a module path (e.g., `app/services/portfolio_service.py`).

Steps:
1. Read the target module to understand its functions and dependencies.
2. Identify testable units: public functions, edge cases, error paths.
3. Create or update the test file in `backend/tests/test_{module_name}.py`.
4. Follow project testing conventions:
   - Use `db` fixture for service tests, `client` fixture for E2E tests.
   - Use `make_tx()` factory for transaction inputs.
   - AAA pattern: Arrange, Act, Assert.
   - Naming: `test_{function}_{scenario}`.
5. Run the new tests with `cd backend && uv run pytest -v tests/test_{module_name}.py`.
6. Report results and fix any failures.
