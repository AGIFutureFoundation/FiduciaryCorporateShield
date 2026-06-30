from abc import ABC, abstractmethod
from typing import Any, Dict

class Agent(ABC):
    """
    Minimal Agent interface.
    Implementations should be deterministic and side-effect-free where possible,
    so they're easy to test. Real agents can async out to LLMs or other services.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def run(self, input: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Run the agent with a text input and optional context.

        Returns a dict with structured output, e.g. {"output": "...", "meta": {...}}
        """
        raise NotImplementedError
