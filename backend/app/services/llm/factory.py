"""Factory function to create the appropriate LLM provider."""

from app.config import Settings
from app.constants import LLMProviderType
from app.services.llm.base import LLMProvider


def create_llm_provider(settings: Settings) -> LLMProvider:
    """Instantiate an LLM provider based on application settings.

    Args:
        settings: Application settings with LLM configuration.

    Returns:
        A concrete LLMProvider instance.
    """
    match settings.LLM_PROVIDER:
        case LLMProviderType.ANTHROPIC:
            from app.services.llm.anthropic_provider import AnthropicProvider

            return AnthropicProvider(
                api_key=settings.ANTHROPIC_API_KEY,
                model=settings.LLM_MODEL,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
            )
        case LLMProviderType.OPENAI:
            from app.services.llm.openai_provider import OpenAIProvider

            return OpenAIProvider(
                api_key=settings.OPENAI_API_KEY,
                model=settings.LLM_MODEL,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
            )
        case _:
            from app.services.llm.mock_provider import MockProvider

            return MockProvider()
