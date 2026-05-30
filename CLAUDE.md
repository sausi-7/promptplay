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

### Running the Web Server
```bash
# Start the FastAPI server (web UI on localhost:8000)
python server.py

# Open http://localhost:8000 in browser and enter your game idea
```

### Running CLI (without web server)
```bash
# Edit game_idea in agent.py, then:
python agent.py

# This generates output.html, open it:
open output.html
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

The project has three main components:

### agent.py
- **`build_prompt(game_idea)`**: Wraps a raw game idea with strict instructions to ensure Claude returns only HTML/CSS/JavaScript code without explanations
- **`generate_game_html(game_idea)`**: Calls the Claude Agent SDK's `query()` function with the wrapped prompt
- **`htmlParser(result)`**: Extracts clean HTML from Claude's response (prioritizes html-tagged code blocks)
- **`main()`**: CLI entry point that writes the generated game to `output.html`
- Uses Haiku model by default for speed; no tools enabled (`allowed_tools=[]`) since the agent just generates code

### server.py
- **FastAPI application** that provides a web interface for game generation
- **`POST /generate`**: Accepts `{"game_idea": "..."}`, runs the agent, saves to `output.html`, returns `{"success": true/false}`
- **`GET /game`**: Serves the generated `output.html` with cache-busting headers
- **`GET /`**: Serves the web form (`index.html`)

### index.html
- **Web form** for entering game descriptions
- **Iframe** that displays the generated game (rendered from `/game`)
- **Error handling** and loading states
- **No popup blockers** — games render inline on the page

### Key Dependencies
- `claude-agent-sdk`: Provides the `query()` function and agent orchestration
- `python-dotenv`: Loads ANTHROPIC_API_KEY from .env file
- `fastapi`: Web framework for the server
- `uvicorn`: ASGI server for FastAPI

## Development Workflow

### Testing Game Ideas
1. **Web UI**: Run `python server.py` and type your idea in the browser
2. **CLI**: Edit `game_idea` in `agent.py`, then run `python agent.py`

### Changing Models
- Edit the `model` parameter in `agent.py` inside `generate_game_html()`:
  - `"claude-opus-4-8"` for complex/3D games
  - `"claude-sonnet-4-6"` for balanced performance
  - `"claude-haiku-4-5-20251001"` for quick iteration (default)

### Modifying Prompt Instructions
- Edit `build_prompt()` in `agent.py` to customize how game ideas are converted to Claude instructions
- The function wraps user input with strict directives to ensure HTML-only output

### Before Committing
1. Run the import check: `python -c "import agent; import server; print('✓ All imports OK')"`
2. Run ruff linting: `ruff check . --select=E9,F63,F7,F82`
3. Test: `python agent.py` generates a valid HTML game

## Testing & CI

- CI runs on Python 3.10, 3.11, 3.12
- Tests verify: imports work, ruff linting passes
- No dedicated test suite yet (see CONTRIBUTING.md for good first issues)

## Key Files

- `agent.py` – Core game generation using Claude Agent SDK
  - `build_prompt()` – Wraps game ideas with strict instructions
  - `generate_game_html()` – Async function that calls Claude
  - `htmlParser()` – Extracts HTML from Claude's response
  
- `server.py` – FastAPI web server
  - `POST /generate` – Game generation endpoint
  - `GET /game` – Serves generated game
  - `GET /` – Serves web UI
  
- `index.html` – Web interface for game generation
  - Form for entering game ideas
  - Iframe for displaying games
  - Error handling and loading states
  
- `requirements.txt` – Dependencies (includes fastapi, uvicorn, claude-agent-sdk)
- `.env.example` – Template for API key configuration
- `CHANGELOG.md` – Version history
- `CONTRIBUTING.md` – Guidelines for contributors
