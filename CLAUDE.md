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

### Running CLI - Quick Mode (One-Shot)
```bash
# Edit game_idea in agent.py, then:
python agent.py

# This generates output.html, open it:
open output.html
```

### Running CLI - Conversational Mode (Recommended)
```bash
# Interactive mode with clarifying questions:
python conversation_agent.py

# You'll be prompted to:
# 1. Describe your game idea
# 2. Answer Claude's clarifying questions
# 3. Review the generated game
# 4. Request refinements if needed (optional)
# 5. Save the final game

# Your conversation is saved to games/{game_id}_memory.json
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
- **Mode**: One-shot generation (quick, no iterations)
- Uses Haiku model by default for speed; no tools enabled (`allowed_tools=[]`)

### conversation_agent.py
- **`ConversationMemory`**: Stores conversation history in JSON format (`games/{game_id}_memory.json`)
  - Tracks game idea, clarifications, generations, and refinements
- **`build_clarification_prompt()`**: Generates prompt for Claude to ask smart clarifying questions
- **`build_generation_prompt()`**: Generates final game based on all collected info
- **`build_refinement_prompt()`**: Generates improved version based on user feedback
- **`ask_clarifications()`**: Interactive Q&A with Claude about the game
- **`generate_game()`**: Creates initial game with clarifications
- **`refine_game()`**: Iterative refinement loop for user feedback
- **Mode**: Conversational with memory (slower, higher quality, allows iterations)
- Uses Haiku model; perfect for exploring game ideas before committing

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

## Two Modes Explained

### Mode 1: One-Shot (agent.py)
- **Best for**: Quick iterations, CLI scripts, simple games
- **Process**: Idea → Generate → Done
- **Time**: ~5-10 seconds
- **Quality**: Good (follows 10 requirements)

### Mode 2: Conversational (conversation_agent.py)
- **Best for**: Refining game ideas, building exactly what you want, exploring possibilities
- **Process**: Idea → Clarifying Q&A → Generate → Refine → Refine → Done
- **Time**: ~30-60 seconds + refinement time
- **Quality**: Excellent (tailored to your specifications)
- **Memory**: Full conversation saved for reference

## Key Files

- `agent.py` – One-shot game generation using Claude Agent SDK
  - `build_prompt()` – Wraps game ideas with strict instructions
  - `generate_game_html()` – Async function that calls Claude
  - `htmlParser()` – Extracts HTML from Claude's response

- `conversation_agent.py` – Conversational game generation with memory
  - `ConversationMemory` – Stores all conversation history
  - `ask_clarifications()` – Claude asks smart questions
  - `generate_game()` – Creates game based on answers
  - `refine_game()` – Iterative refinement loop
  
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
