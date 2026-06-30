from typing import Dict, Any
from .agent_base import Agent

class EchoAgent(Agent):
    @property
    def name(self) -> str:
        return "echo"

    async def run(self, input: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        # Simple example: returns original input and a reversed version.
        reversed_text = input[::-1] if input is not None else ""
        return {"output": input, "reversed": reversed_text, "meta": {"len": len(input or "")}}
