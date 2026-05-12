"""Pydantic model for validated LLM output."""

from pydantic import BaseModel, Field


class InsightResponse(BaseModel):
    """Structured LLM output for portfolio insights.

    Validates that the LLM response conforms to expected types
    and constraints regardless of provider.
    """

    summary: str
    recommendations: list[str] = Field(max_length=3)
    risk_score: int = Field(ge=1, le=10)
    highlights: list[str] = Field(max_length=3)
