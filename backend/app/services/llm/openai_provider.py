"""OpenAI LLM provider stub for future extensibility."""

from app.schemas.llm import InsightResponse
from app.services.llm.base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI provider stub — demonstrates extensibility of the factory pattern."""

    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int):
        self._api_key = api_key
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

    def generate_insights(
        self, prompt: str, system_prompt: str = ""
    ) -> InsightResponse:
        raise NotImplementedError(
            "OpenAI provider is a stub for future use. "
            "Set LLM_PROVIDER=anthropic or LLM_PROVIDER=mock."
        )
