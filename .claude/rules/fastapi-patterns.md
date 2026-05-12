---
globs: backend/app/api/**/*.py
---

# FastAPI Route Patterns

- All endpoints return `ApiResponse[T]` envelope from `app/schemas/base.py`.
- Inject DB sessions via `db: Session = Depends(get_db)` from `app/dependencies.py`.
- Routes are thin controllers — delegate to service functions in `app/services/`.
- Raise `AppException` subclasses for errors; global handlers convert to JSON.
- Exception types: `UploadError` (400), `ValidationError` (422), `NotFoundError` (404).
- Use `ErrorCode` enum values for error codes, never raw strings.
- Paginated endpoints accept `page` and `page_size` query params; return `PaginationMeta`.
- File uploads use `UploadFile` parameter; validate size/extension before processing.
- Group routes in an `APIRouter` with prefix and tags; combine in `v1/router.py`.
