"""Deterministic mock LLM provider for development and testing."""

from app.schemas.llm import InsightResponse
from app.services.llm.base import LLMProvider


class MockProvider(LLMProvider):
    """Returns deterministic mock insights without any API calls.

    Used as the default provider and as a fallback when real
    providers fail validation.
    """

    def generate_insights(self, prompt: str) -> InsightResponse:
        return InsightResponse(
            summary="Mock analysis: portfolio appears stable with moderate diversification.",
            recommendations=[
                "Review concentration risk in top holdings.",
                "Consider rebalancing to reduce single-ISIN exposure.",
                "Monitor violation alerts for compliance issues.",
            ],
            risk_score=4,
            highlights=[
                "Portfolio health: stable",
                "Diversification: moderate",
                "Compliance: review needed",
            ],
        )
