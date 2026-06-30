import asyncio
from agents.example_agent import EchoAgent

import pytest


def test_echo_agent():
    agent = EchoAgent()
    res = asyncio.run(agent.run("hello"))
    assert res["output"] == "hello"
    assert res["reversed"] == "olleh"
    assert res["meta"]["len"] == 5
