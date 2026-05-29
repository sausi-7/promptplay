# promptplay

> Transform natural language prompts into playable games using Claude

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/sausi-7/promptplay/blob/main/CONTRIBUTING.md)

## What is promptplay?

promptplay is a creative playground that leverages the [Claude Agent SDK](https://github.com/anthropics/anthropic-sdk-python) to turn natural language descriptions into fully functional games. Describe the game you want to build—a Snake game, Flappy Bird, a puzzle game—and Claude will write the complete implementation for you.

## How It Works

```
Your Prompt
    ↓
Claude Agent SDK
    ↓
Claude Code (with Bash & file tools)
    ↓
Game Code (HTML/JavaScript)
    ↓
Playable Game 🎮
```

The magic happens through multi-step agent interactions: Claude reads your prompt, executes code, and iterates until it delivers a complete, working game.

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

```bash
python agent.py
```

The script will print the generated game code to stdout. You can redirect it to a file:

```bash
python agent.py > my_game.html
open my_game.html
```

## Examples

Try these prompts by editing the `prompt` string in `agent.py`:

| Prompt | Output |
|--------|--------|
| `"Build me a snake game in single index.html"` | Classic Snake with keyboard controls |
| `"Create a Flappy Bird-style game"` | Bird dodging obstacles |
| `"Build a memory matching card game"` | Click-to-flip matching game |
| `"Make a simple Pong game"` | Two-player paddle game |

## Extending It

### Change the Prompt

Edit the `prompt` parameter in `agent.py`:

```python
prompt="Your game idea here"
```

### Adjust the Model

Use a different Claude model by changing the `model` parameter:

```python
model="claude-opus-4-7"  # For more complex games
model="claude-haiku-4-5-20251001"  # For quick, lightweight games
```

### Enable More Tools

The SDK can use additional tools. Extend `allowed_tools` in `agent.py`:

```python
allowed_tools=["Bash", "Glob", "Read", "Write"]
```

## Roadmap

- [ ] Web UI to input prompts and play games directly
- [ ] Multi-file game support (separate HTML, CSS, JS)
- [ ] Prompt gallery: community-submitted game ideas
- [ ] CLI flags to customize model, effort, and output
- [ ] Game examples directory with pre-generated games
- [ ] Streaming output for real-time generation feedback

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
