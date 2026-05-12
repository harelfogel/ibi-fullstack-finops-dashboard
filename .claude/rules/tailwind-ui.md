---
globs: frontend/src/components/**/*.tsx
---

# Tailwind & UI Conventions

- Dark theme by default — root has `dark` class, use `bg-slate-950`, `bg-slate-900`, `bg-slate-800`.
- Text colors: `text-white`, `text-slate-300`, `text-slate-400` for hierarchy.
- Accent palette: emerald for positive/success, red for negative/error, amber for warnings.
- P&L coloring: use `pnlColor()` from `lib/utils/format.ts` — green for gains, red for losses.
- Use `cn()` utility for conditional class composition (clsx-based).
- Reusable UI primitives in `components/ui/`: Card, Badge, Spinner, Skeleton, EmptyState, ProgressBar.
- Badge variants: `success`, `error`, `warning` — map to severity/status.
- Finance aesthetic: clean data tables, numeric alignment, subtle borders, card-based layouts.
- Responsive: sidebar collapses on mobile, tables scroll horizontally.
