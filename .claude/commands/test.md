Run the backend test suite and report results.

Steps:
1. Run `cd backend && uv run pytest -v` to execute all tests.
2. Report total pass/fail count.
3. If any tests fail, analyze the failure output:
   - Identify the failing test name and file.
   - Show the assertion error or exception.
   - Suggest a fix based on the error.
4. If all tests pass, confirm the count (expected: 31 tests).
