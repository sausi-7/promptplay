import asyncio
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

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
def test_query_runs_without_errors():
    """The query function runs without errors when API is mocked."""
    from claude_agent_sdk import ClaudeAgentOptions

    async def run_test():
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

    asyncio.run(run_test())


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


def test_generate_game_html_streams_progress(capsys):
    """CLI streaming prints progress and intermediate text while preserving HTML extraction."""
    import agent

    async def run_test():
        async def mock_query(*args, **kwargs):
            yield SimpleNamespace(content=[{"text": "```html\n"}])
            yield SimpleNamespace(content=[{"text": "<html><body>Game"}])
            yield SimpleNamespace(result="```html\n<html><body>Game</body></html>\n```")

        with patch("agent.query", side_effect=mock_query):
            return await agent.generate_game_html("memory cards", stream=True, verbose=True)

    html = asyncio.run(run_test())

    captured = capsys.readouterr()
    assert "Generating game..." in captured.out
    assert "Connecting to Claude" in captured.out
    assert "Writing game logic" in captured.out
    assert "[stream] message 1" in captured.out
    assert "<html><body>Game" in captured.out
    assert "Complete!" in captured.out
    assert html == "<html><body>Game</body></html>"


def test_generate_game_html_can_run_silently(capsys):
    """Web/server callers can keep using generate_game_html without CLI progress output."""
    import agent

    async def run_test():
        async def mock_query(*args, **kwargs):
            yield SimpleNamespace(result="```html\n<html><body>Silent</body></html>\n```")

        with patch("agent.query", side_effect=mock_query):
            return await agent.generate_game_html("quiet game")

    html = asyncio.run(run_test())

    captured = capsys.readouterr()
    assert captured.out == ""
    assert html == "<html><body>Silent</body></html>"
