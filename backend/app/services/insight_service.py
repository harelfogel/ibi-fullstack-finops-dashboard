"""AI-powered portfolio insight service with mock fallback."""

import logging
from decimal import Decimal

from sqlalchemy.orm import Session

from app.config import settings
from app.models.portfolio_position import PortfolioPosition
from app.models.violation import Violation
from app.services.portfolio_service import get_portfolio_summary

logger = logging.getLogger(__name__)


def get_client_insights(client_id: str, db: Session) -> dict:
    """Generate AI insights for a client's portfolio.

    Uses Anthropic Claude API if configured, otherwise falls back to
    deterministic mock insights.

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

    if not settings.AI_MOCK_MODE and settings.ANTHROPIC_API_KEY:
        try:
            return _generate_ai_insights(client_id, positions, violations, summary)
        except Exception:
            logger.exception("AI insight generation failed, falling back to mock")

    return _generate_mock_insights(client_id, positions, violations, summary)


def _generate_ai_insights(
    client_id: str,
    positions: list[PortfolioPosition],
    violations: list[Violation],
    summary: dict,
) -> dict:
    """Generate insights using Anthropic Claude API."""
    import anthropic

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    portfolio_text = "\n".join(
        f"- {p.isin}: {p.current_quantity} units, avg cost {p.average_cost}, "
        f"market value {p.market_value}, realized P&L {p.realized_pnl}"
        for p in positions
    )

    violation_text = "\n".join(
        f"- [{v.severity}] {v.violation_type}: {v.message}" for v in violations
    ) or "No violations detected."

    prompt = f"""Analyze this client's portfolio and provide investment insights.

Client: {client_id}
Total Portfolio Value: {summary['total_value']}
Realized P&L: {summary['total_realized_pnl']}
Unrealized P&L: {summary['total_unrealized_pnl']}

Positions:
{portfolio_text}

Violations:
{violation_text}

Provide a JSON response with:
1. "summary": A 2-3 sentence portfolio health overview
2. "recommendations": Array of 2-3 actionable recommendations
3. "risk_score": Number 1-10 (1=low risk, 10=high risk)
4. "highlights": Array of 2-3 key observations"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    import json

    try:
        response_text = message.content[0].text
        # Try to extract JSON from the response
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(response_text[start:end])
    except (json.JSONDecodeError, IndexError):
        pass

    return {
        "summary": message.content[0].text,
        "recommendations": [],
        "risk_score": 5,
        "highlights": [],
    }


def _generate_mock_insights(
    client_id: str,
    positions: list[PortfolioPosition],
    violations: list[Violation],
    summary: dict,
) -> dict:
    """Generate deterministic mock insights based on portfolio data."""
    total_value = summary["total_value"]
    realized_pnl = summary["total_realized_pnl"]
    unrealized_pnl = summary["total_unrealized_pnl"]
    position_count = summary["position_count"]

    # Calculate risk score based on violations and concentration
    risk_score = 3  # Base risk
    error_violations = [v for v in violations if v.severity == "error"]
    warning_violations = [v for v in violations if v.severity == "warning"]
    risk_score += len(error_violations) * 2
    risk_score += len(warning_violations)
    risk_score = min(risk_score, 10)

    # Build summary
    pnl_direction = "positive" if (realized_pnl + unrealized_pnl) >= 0 else "negative"
    violation_note = ""
    if violations:
        violation_note = (
            f" There are {len(violations)} active violation(s) that require attention."
        )

    summary_text = (
        f"Client {client_id} holds {position_count} position(s) with a total "
        f"portfolio value of ${total_value:,.2f}. Overall P&L trend is {pnl_direction} "
        f"with ${realized_pnl:,.2f} realized and ${unrealized_pnl:,.2f} unrealized gains."
        f"{violation_note}"
    )

    # Build recommendations
    recommendations = []
    if error_violations:
        recommendations.append(
            "Address short-selling violations immediately to ensure regulatory compliance."
        )
    if any(v.violation_type == "concentration_risk" for v in violations):
        recommendations.append(
            "Consider diversifying holdings to reduce concentration risk below 50%."
        )
    if any(v.violation_type == "day_trading" for v in violations):
        recommendations.append(
            "Review day-trading patterns and consider implementing trade frequency controls."
        )
    if position_count == 1:
        recommendations.append(
            "Portfolio is highly concentrated in a single position. "
            "Diversification across multiple ISINs is recommended."
        )
    if realized_pnl < 0:
        recommendations.append(
            "Review loss-making positions for potential tax-loss harvesting opportunities."
        )
    if not recommendations:
        recommendations.append(
            "Portfolio appears well-managed. Continue monitoring for any emerging risks."
        )

    # Build highlights
    highlights = []
    if total_value > 0:
        highlights.append(f"Portfolio value: ${total_value:,.2f}")
    if realized_pnl != 0:
        highlights.append(
            f"Realized P&L: {'+'if realized_pnl > 0 else ''}${realized_pnl:,.2f}"
        )
    if violations:
        highlights.append(f"{len(violations)} violation(s) detected")
    if position_count > 0:
        highlights.append(f"{position_count} active position(s)")

    return {
        "summary": summary_text,
        "recommendations": recommendations[:3],
        "risk_score": risk_score,
        "highlights": highlights[:3],
    }
