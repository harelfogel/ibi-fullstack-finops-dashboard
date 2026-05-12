Scaffold a full-stack endpoint from backend route to frontend hook.

Ask the user for:
- Resource name (e.g., "reports")
- HTTP method and path
- Request/response shape description

Then create or update these files in order:

1. **Pydantic schema** — `backend/app/schemas/{resource}.py`
   - Response model with `model_config = {"from_attributes": True}`
2. **Service function** — `backend/app/services/{resource}_service.py`
   - Business logic with DB session parameter
3. **Route handler** — `backend/app/api/v1/{resource}.py`
   - Thin controller returning `ApiResponse[T]`
   - Register in `backend/app/api/v1/router.py`
4. **TypeScript type** — `frontend/src/types/{resource}.ts`
   - Interface matching the Pydantic schema
5. **API function** — `frontend/src/lib/api/{resource}.ts`
   - Typed fetch call using the `api` client
6. **TanStack Query hook** — `frontend/src/lib/hooks/use{Resource}.ts`
   - `useQuery` or `useMutation` as appropriate

Follow all project conventions (response envelope, error handling, naming).
