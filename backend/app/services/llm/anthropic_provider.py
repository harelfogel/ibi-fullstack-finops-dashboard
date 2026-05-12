"""Anthropic Claude LLM provider."""

import json
import logging

import anthropic

from app.schemas.llm import InsightResponse
from app.services.llm.base import LLMProvider

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    """Generate insights using Anthropic Claude API."""

    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int):
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

    def generate_insights(self, prompt: str) -> InsightResponse:
        message = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text

        # Extract JSON from response
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start < 0 or end <= start:
            raise ValueError("No JSON object found in LLM response")

        raw = json.loads(response_text[start:end])
        return InsightResponse.model_validate(raw)
