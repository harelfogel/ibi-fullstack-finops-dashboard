# Error Handling Patterns

## Backend Exception Hierarchy
- `AppException` (base) -> `UploadError` (400), `ValidationError` (422), `NotFoundError` (404).
- Always use `ErrorCode` enum values — never raw strings for error codes.
- Global handlers in `exceptions.py` convert exceptions to `ApiResponse` JSON envelope.
- Raise specific exceptions: `raise NotFoundError(ErrorCode.CLIENT_NOT_FOUND, "...")`.

## Service Layer Error Handling
- Services catch expected failures and raise `AppException` subclasses.
- Unexpected errors propagate to global handler as 500 with `ErrorCode.INTERNAL_ERROR`.
- LLM service wraps provider calls in try/except with MockProvider fallback.
- Upload pipeline: validate first, persist only valid rows, report errors in response.

## Frontend Error Handling
- API client throws typed `ApiError` with `code`, `message`, `status` fields.
- Components handle three states: `{ data, isLoading, error }` from TanStack Query.
- Mutations use try/catch with `addToast("error", message)` for user feedback.
- Never swallow errors silently — always show feedback via toast or inline error.

## Logging Standards
- Use `logging.getLogger(__name__)` per module.
- `logger.exception()` for caught errors with stack traces.
- `logger.warning()` for recoverable issues (e.g., LLM fallback to mock).
- `logger.info()` for significant operations (upload processed, portfolio recalculated).
- Never log API keys, credentials, or sensitive user data.
