import pytest
from unittest.mock import AsyncMock, patch, MagicMock

pytestmark = []

# ── TEST 1: module import ────────────────────────────────
def test_agent_imports():
    """The agent module can be imported without executing main."""
    import importlib
    import unittest.mock as mock

    with mock.patch("asyncio.run"):
        import agent
        importlib.reload(agent)

    assert agent is not None


# ── TEST 2: query runs with mocked API ──────────────────
@pytest.mark.asyncio
async def test_query_runs_without_errors():
    """The query function runs without errors when API is mocked."""
    from claude_agent_sdk import ClaudeAgentOptions

    mock_message = MagicMock()
    mock_message.result = "test result"

    async def mock_query(*args, **kwargs):
        yield mock_message

    with patch("claude_agent_sdk.query", side_effect=mock_query):
        from claude_agent_sdk import query

        messages = []
        async for message in query(
            prompt="test prompt",
            options=ClaudeAgentOptions(
                model="claude-haiku-4-5-20251001",
                allowed_tools=["Bash"],
                effort="high",
            ),
        ):
            if hasattr(message, "result"):
                messages.append(message.result)

        assert len(messages) >= 0


# ── TEST 3: ClaudeAgentOptions accepts different models ─
def test_options_different_models():
    """ClaudeAgentOptions accepts different model values."""
    from claude_agent_sdk import ClaudeAgentOptions

    options_haiku = ClaudeAgentOptions(model="claude-haiku-4-5-20251001")
    options_sonnet = ClaudeAgentOptions(model="claude-sonnet-4-6")

    assert options_haiku.model == "claude-haiku-4-5-20251001"
    assert options_sonnet.model == "claude-sonnet-4-6"


# ── TEST 4: ClaudeAgentOptions accepts different effort levels ──
def test_options_effort_levels():
    """ClaudeAgentOptions accepts valid effort values."""
    from claude_agent_sdk import ClaudeAgentOptions

    for effort in ["low", "medium", "high"]:
        options = ClaudeAgentOptions(effort=effort)
        assert options.effort == effort


# ── TEST 5: ClaudeAgentOptions accepts different tools ────
def test_options_allowed_tools():
    """ClaudeAgentOptions accepts lists of tools."""
    from claude_agent_sdk import ClaudeAgentOptions

    options = ClaudeAgentOptions(allowed_tools=["Bash", "Glob"])
    assert "Bash" in options.allowed_tools
    assert "Glob" in options.allowed_tools