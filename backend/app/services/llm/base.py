"""Abstract base class for LLM providers."""

from abc import ABC, abstractmethod

from app.schemas.llm import InsightResponse


class LLMProvider(ABC):
    """Base class all LLM providers must implement."""

    @abstractmethod
    def generate_insights(self, prompt: str) -> InsightResponse:
        """Generate portfolio insights from a prompt.

        Args:
            prompt: Formatted portfolio analysis prompt.

        Returns:
            Validated InsightResponse with summary, recommendations,
            risk_score, and highlights.
        """
