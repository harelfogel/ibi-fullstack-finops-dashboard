"""AI-powered portfolio insight service using generic LLM factory."""

import logging

from sqlalchemy.orm import Session

from app.config import settings
from app.models.portfolio_position import PortfolioPosition
from app.models.violation import Violation
from app.services.llm import create_llm_provider
from app.services.llm.mock_provider import MockProvider
from app.services.portfolio_service import get_portfolio_summary

logger = logging.getLogger(__name__)


def get_client_insights(client_id: str, db: Session) -> dict:
    """Generate AI insights for a client's portfolio.

    Uses the configured LLM provider (Anthropic, OpenAI, or mock).
    Falls back to mock if the provider fails or returns invalid output.

    Args:
        client_id: The client identifier.
        db: Database session.

    Returns:
        Dict with summary, recommendations, risk_score, and highlights.
    """
    positions = (
        db.query(PortfolioPosition)
        .filter(PortfolioPosition.client_id == client_id)
        .all()
    )

    violations = (
        db.query(Violation)
        .filter(Violation.client_id == client_id)
        .all()
    )

    summary = get_portfolio_summary(client_id, db)
    prompt = build_portfolio_prompt(client_id, positions, violations, summary)

    provider = create_llm_provider(settings)

    try:
        result = provider.generate_insights(prompt)
    except Exception:
        if not isinstance(provider, MockProvider):
            logger.exception("LLM provider failed, falling back to mock")
            result = MockProvider().generate_insights(prompt)
        else:
            raise

    return result.model_dump()


def build_portfolio_prompt(
    client_id: str,
    positions: list[PortfolioPosition],
    violations: list[Violation],
    summary: dict,
) -> str:
    """Build the prompt sent to the LLM provider.

    Reusable across providers — always requests structured JSON output.
    """
    portfolio_text = "\n".join(
        f"- {p.isin}: {p.current_quantity} units, avg cost {p.average_cost}, "
        f"market value {p.market_value}, realized P&L {p.realized_pnl}"
        for p in positions
    )

    violation_text = "\n".join(
        f"- [{v.severity}] {v.violation_type}: {v.message}" for v in violations
    ) or "No violations detected."

    return f"""Analyze this client's portfolio and provide investment insights.

Client: {client_id}
Total Portfolio Value: {summary['total_value']}
Realized P&L: {summary['total_realized_pnl']}
Unrealized P&L: {summary['total_unrealized_pnl']}

Positions:
{portfolio_text}

Violations:
{violation_text}

Respond with ONLY a JSON object (no markdown, no explanation) containing:
1. "summary": A 2-3 sentence portfolio health overview
2. "recommendations": Array of 2-3 actionable recommendations
3. "risk_score": Number 1-10 (1=low risk, 10=high risk)
4. "highlights": Array of 2-3 key observations"""
