from typing import Protocol


class CompletionProvider(Protocol):
    def complete(self, prompt: str) -> str | None: ...


class LLMClient:
    """Provider-independent seam. Add provider adapters here, never in risk logic."""
    def __init__(self, provider: str = "disabled", api_key: str | None = None, model: str | None = None):
        self.provider, self.api_key, self.model = provider, api_key, model

    def complete(self, prompt: str) -> str | None:
        if self.provider == "disabled":
            return None
        raise NotImplementedError(f"LLM provider '{self.provider}' is not configured")
