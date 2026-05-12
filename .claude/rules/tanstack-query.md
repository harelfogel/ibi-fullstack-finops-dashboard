---
globs: frontend/src/lib/hooks/**/*.ts
---

# TanStack Query v5 Conventions

- Use `useQuery` for GET requests, `useMutation` for POST/PUT/DELETE.
- Query keys are arrays: `["clients"]`, `["portfolio", clientId]`.
- Query functions call typed API helpers from `lib/api/` — never raw `fetch`.
- Default config in `QueryProvider.tsx`: 30s staleTime, 1 retry, no refetchOnWindowFocus.
- Mutations invalidate related queries via `queryClient.invalidateQueries()`.
- Enable queries conditionally: `enabled: !!clientId` when param may be undefined.
- Return the full hook result (`{ data, isLoading, error }`) — let components handle states.
- One hook per resource file: `useClients.ts`, `usePortfolio.ts`, etc.
