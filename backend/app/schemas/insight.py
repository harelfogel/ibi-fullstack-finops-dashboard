"""Insight response schemas."""

from pydantic import BaseModel


class InsightOut(BaseModel):
    summary: str
    recommendations: list[str]
    risk_score: int
    highlights: list[str]
