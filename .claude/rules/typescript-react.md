---
globs: frontend/src/**/*.{ts,tsx}
---

# TypeScript & React Conventions

- TypeScript strict mode is enabled — no `any` types, handle all nullable cases.
- Use named exports, not default exports (except Next.js pages which require default).
- Components are function components with explicit return types where non-trivial.
- Props interfaces: `interface FooProps { ... }` defined above the component.
- Use `"use client"` directive only on components that use hooks or browser APIs.
- Path aliases: `@/` maps to `src/` (configured in tsconfig.json).
- Types mirror backend schemas in `src/types/` — keep them in sync.
- Format numbers with utilities from `lib/utils/format.ts`: `formatCurrency`, `pnlColor`, `pnlSign`.
- Use `cn()` from `lib/utils/cn.ts` for conditional Tailwind class merging.
