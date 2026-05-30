# promptplay

> Transform natural language prompts into playable games using Claude

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/sausi-7/promptplay/blob/main/CONTRIBUTING.md)

## What is promptplay?

promptplay is a creative playground that leverages the [Claude Agent SDK](https://github.com/anthropics/anthropic-sdk-python) to turn natural language descriptions into fully functional games. Describe the game you want to build—a Snake game, Flappy Bird, a puzzle game—and Claude will write the complete implementation for you.

## How It Works

### Web Interface (Recommended)
```
Your Game Idea
    ↓
Web Form (index.html)
    ↓
/generate endpoint (server.py)
    ↓
Claude Agent SDK generates HTML/CSS/JS
    ↓
Saved to output.html
    ↓
Rendered in iframe on page 🎮
```

### CLI Mode
```
Edit agent.py with your game idea
    ↓
python agent.py
    ↓
Claude generates complete game code
    ↓
Saved to output.html
    ↓
Open in browser 🎮
```

The agent automatically wraps your game idea with strict instructions to ensure Claude returns only clean HTML/CSS/JavaScript code without explanations or tool usage.

## Quick Start

### Prerequisites

- Python 3.10+
- An Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

```bash
# Clone the repository
git clone https://github.com/sausi-7/promptplay.git
cd promptplay

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Edit .env and paste your ANTHROPIC_API_KEY
```

### Running

#### Option 1: Web Server (Recommended)

Start the FastAPI server:
```bash
python server.py
# Server runs on http://localhost:8000
```

Open your browser and describe your game idea. The generated game will render instantly in the page.

#### Option 2: Command Line

Edit the game idea in `agent.py` and run:
```bash
python agent.py
# Generates output.html
open output.html
```

## Examples

Try these prompts by editing the `prompt` string in `agent.py`:

| Prompt | Output |
|--------|--------|
| `"Build me a snake game in single index.html"` | Classic Snake with keyboard controls |
| `"Create a Flappy Bird-style game"` | Bird dodging obstacles |
| `"Build a memory matching card game"` | Click-to-flip matching game |
| `"Make a simple Pong game"` | Two-player paddle game |

## Architecture

### Key Components

- **agent.py** - Core game generation using Claude Agent SDK
  - `build_prompt()` - Wraps user ideas with strict instructions to ensure HTML-only output
  - `generate_game_html()` - Calls Claude to generate complete game code
  - `htmlParser()` - Extracts clean HTML from Claude's response
  
- **server.py** - FastAPI web server with two endpoints
  - `POST /generate` - Accepts a game idea, runs the agent, returns success/failure
  - `GET /game` - Serves the generated `output.html` file
  - `GET /` - Serves the web UI
  
- **index.html** - Web interface for submitting game ideas
  - Form for entering game descriptions
  - Iframe rendering of generated games
  - Error handling and loading states

## Customization

### Change the Game Idea (CLI)

Edit the `game_idea` in `agent.py`:

```python
game_idea = "Your detailed game description here"
html = await generate_game_html(game_idea)
```

### Adjust the Model

Change the `model` parameter in `agent.py`:

```python
model="claude-opus-4-8"      # For complex/3D games
model="claude-sonnet-4-6"    # Balanced performance
model="claude-haiku-4-5-20251001"  # Fast, lightweight
```

### Modify Prompt Instructions

Edit `build_prompt()` in `agent.py` to customize how game ideas are converted to instructions.

## Roadmap

- [x] Web UI to input prompts and play games directly
- [x] FastAPI server with endpoints for game generation
- [x] Iframe-based game rendering (no popup blockers)
- [ ] Multi-file game support (separate HTML, CSS, JS)
- [ ] Prompt gallery: community-submitted game ideas
- [ ] CLI flags to customize model, effort, and output
- [ ] Game examples directory with pre-generated games
- [ ] Streaming output for real-time generation feedback
- [ ] Game save/download functionality
- [ ] Share generated games via URL

## Contributing

We love contributions! Whether you're fixing bugs, adding features, or sharing cool game prompts—all are welcome.

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-game-idea`)
3. Make your changes
4. Commit with a clear message (`git commit -m "Add support for X"`)
5. Push to your fork and open a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Good First Issues

- [ ] Add a new example prompt to the README
- [ ] Create a prompt template for different game genres
- [ ] Add error handling for API failures
- [ ] Write tests for the agent module
- [ ] Improve documentation

## License

This project is licensed under the MIT License—see [LICENSE](LICENSE) for details.

## Questions?

Open an issue on [GitHub](https://github.com/sausi-7/promptplay/issues) or reach out to [@sausi-7](https://github.com/sausi-7).

---

Built with ❤️ and the [Claude Agent SDK](https://github.com/anthropics/anthropic-sdk-python)
