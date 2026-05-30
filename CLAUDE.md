# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**promptplay** is a tool that uses the [Claude Agent SDK](https://github.com/anthropics/anthropic-sdk-python) to transform natural language prompts into fully functional, playable games. The agent receives a game description, uses Claude to write complete HTML/JavaScript game code, and outputs the result.

## Setup & Common Commands

### Initial Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Running the Agent
```bash
# Generate a game from the current prompt in agent.py
python agent.py

# Redirect output to an HTML file and open it
python agent.py > my_game.html && open my_game.html
```

### Code Quality
```bash
# Check for import errors (run by CI)
python -c "import agent; print('✓ All imports OK')"

# Lint with ruff (only checks critical issues: syntax, undefined names, etc.)
pip install ruff
ruff check . --select=E9,F63,F7,F82 --show-source
```

## Architecture

The project is minimal and focused:

- **agent.py**: Single entry point using the Claude Agent SDK
  - Uses `query()` async function with ClaudeAgentOptions
  - Configurable model, allowed_tools, and effort level
  - Streams responses and prints the result (typically HTML game code)
  - Currently set to Haiku model for quick iteration

- **Key Dependencies**:
  - `claude-agent-sdk`: Provides the `query()` function and agent orchestration
  - `python-dotenv`: Loads ANTHROPIC_API_KEY from .env file

## Development Workflow

1. **To test a prompt**: Edit the `prompt` string in `agent.py`, then run `python agent.py`
2. **To switch models**: Change the `model` parameter (e.g., `"claude-opus-4-8"` for complex games)
3. **To enable more tools**: Add tools to `allowed_tools` list (e.g., `["Bash", "Glob", "Read", "Write"]`)
4. **Before committing**: Run the import check and verify the code runs without errors

## Testing & CI

- CI runs on Python 3.10, 3.11, 3.12
- Tests verify: imports work, ruff linting passes
- No dedicated test suite yet (see CONTRIBUTING.md for good first issues)

## Key Files

- `agent.py` – Main agent logic (async query to Claude)
- `requirements.txt` – Dependencies
- `.env.example` – Template for API key configuration
- `CHANGELOG.md` – Version history
- `CONTRIBUTING.md` – Guidelines for contributors
