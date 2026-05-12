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
    system_prompt = build_system_prompt()
    prompt = build_portfolio_prompt(client_id, positions, violations, summary)

    provider = create_llm_provider(settings)

    try:
        result = provider.generate_insights(prompt, system_prompt)
    except Exception:
        if not isinstance(provider, MockProvider):
            logger.exception("LLM provider failed, falling back to mock")
            result = MockProvider().generate_insights(prompt)
        else:
            raise

    return result.model_dump()


def build_system_prompt() -> str:
    """Build the system prompt that defines the AI's role and behavior."""
    return (
        "You are a senior financial operations analyst at Lumina Capital, "
        "an institutional investment firm. You specialize in portfolio risk "
        "assessment, compliance monitoring, and actionable investment guidance.\n\n"
        "Your responsibilities:\n"
        "- Analyze client portfolios using FIFO-based cost accounting\n"
        "- Identify concentration risk, short-selling violations, and day-trading patterns\n"
        "- Provide clear, data-driven recommendations suitable for operations teams\n"
        "- Assess risk on a 1-10 scale based on violation severity, diversification, and P&L trends\n\n"
        "Rules:\n"
        "- Be precise with numbers — reference actual values from the data\n"
        "- Flag any compliance violations as high priority\n"
        "- Recommendations must be actionable (specific ISINs, quantities, thresholds)\n"
        "- Keep language professional and concise, suitable for internal dashboards\n"
        "- Respond with ONLY a valid JSON object, no markdown fences, no explanation"
    )


def build_portfolio_prompt(
    client_id: str,
    positions: list[PortfolioPosition],
    violations: list[Violation],
    summary: dict,
) -> str:
    """Build the user prompt with enriched portfolio context."""
    total_value = float(summary["total_value"])

    portfolio_text = "\n".join(
        f"  - {p.isin}: qty={p.current_quantity}, avg_cost=${p.average_cost}, "
        f"market_value=${p.market_value} "
        f"({(float(p.market_value) / total_value * 100):.1f}% of portfolio), "
        f"realized_pnl=${p.realized_pnl}, unrealized_pnl=${p.unrealized_pnl}"
        if total_value > 0
        else f"  - {p.isin}: qty={p.current_quantity}, avg_cost=${p.average_cost}, "
        f"market_value=${p.market_value}, realized_pnl=${p.realized_pnl}, "
        f"unrealized_pnl=${p.unrealized_pnl}"
        for p in positions
    )

    violation_text = "\n".join(
        f"  - [{v.severity.upper()}] {v.violation_type}: {v.message}"
        for v in violations
    ) or "  None detected."

    position_count = len(positions)
    violation_count = len(violations)
    error_violations = sum(1 for v in violations if v.severity == "error")
    warning_violations = violation_count - error_violations

    return f"""Analyze the following client portfolio and generate insights.

CLIENT: {client_id}
PORTFOLIO OVERVIEW:
  Total Value: ${total_value:,.2f}
  Realized P&L: ${float(summary['total_realized_pnl']):,.2f}
  Unrealized P&L: ${float(summary['total_unrealized_pnl']):,.2f}
  Number of Positions: {position_count}
  Active Violations: {violation_count} ({error_violations} errors, {warning_violations} warnings)

POSITIONS (with portfolio weight):
{portfolio_text}

COMPLIANCE VIOLATIONS:
{violation_text}

Respond with a JSON object containing:
{{
  "summary": "2-3 sentence portfolio health overview referencing specific values",
  "recommendations": ["2-3 actionable items referencing specific ISINs and thresholds"],
  "risk_score": <1-10 integer>,
  "highlights": ["2-3 key data-driven observations"]
}}"""
