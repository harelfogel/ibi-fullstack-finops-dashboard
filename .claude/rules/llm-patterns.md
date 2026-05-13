# LLM & Prompt Engineering Patterns

## Provider Architecture
- Factory pattern: `create_llm_provider()` returns Anthropic/OpenAI/Mock based on `LLM_PROVIDER` setting.
- All providers implement `LLMProvider.generate_insights(prompt, system_prompt)` interface.
- Mock provider is the fallback — used automatically when real providers fail.

## System Prompt Design
- Define the AI's role, domain expertise, and behavioral constraints.
- Include output format requirements (JSON-only, no markdown fences).
- Set precision rules: reference actual portfolio values, specific ISINs, thresholds.
- Keep system prompt stable across requests — it defines identity, not data.

## User Prompt Construction
- Enrich with computed context: portfolio weights, violation severity breakdowns, formatted values.
- Structure as labeled blocks: `CLIENT:`, `PORTFOLIO OVERVIEW:`, `POSITIONS:`, `VIOLATIONS:`.
- Include the expected JSON response schema with field descriptions.
- Handle edge cases: zero total value, no positions, no violations.

## Token Management
- Configure `LLM_MAX_TOKENS` in settings (default: 1024 for insights).
- Set `LLM_TEMPERATURE` low (0.2) for consistent, factual financial analysis.
- Model selection via `LLM_MODEL` setting — allows swapping without code changes.

## Response Validation
- Extract JSON with `find("{")` / `rfind("}")` — handles any wrapper text.
- Parse with `json.loads()` then validate via `InsightResponse.model_validate()`.
- Pydantic schema enforces: `risk_score` (1-10), `summary` (string), `recommendations` (list), `highlights` (list).
- Raise `ValueError` if no JSON object found in response.

## Error Handling & Fallback
- Wrap all provider calls in try/except.
- On failure: log exception, fall back to `MockProvider` for graceful degradation.
- Never let LLM errors crash the API — always return a valid response.
- Log at `exception` level for debugging failed LLM calls.

## Configuration (Environment Variables)
- `LLM_PROVIDER`: `"anthropic"` | `"openai"` | `"mock"` — selects provider.
- `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`: API credentials (never commit).
- `LLM_MODEL`: Model identifier (e.g., `claude-sonnet-4-20250514`).
- `LLM_TEMPERATURE`: Float 0-1, lower = more deterministic.
- `LLM_MAX_TOKENS`: Maximum response tokens.
