# Contributing to PrompttoPlay

Thank you for your interest in contributing! We're excited to have you help make PrompttoPlay better.

## Code of Conduct

Please read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing. We're committed to providing a welcoming and inclusive environment.

## Ways to Contribute

### 🐛 Report Bugs

Found a bug? [Open a bug report](https://github.com/sausi-7/promptplay/issues/new?template=bug_report.md) with:
- A clear title describing the problem
- Steps to reproduce
- Expected vs. actual behavior
- Your environment (OS, Python version, API key region)

### 💡 Suggest Features

Have an idea? [Open a feature request](https://github.com/sausi-7/promptplay/issues/new?template=feature_request.md) with:
- A clear description of what you want and why
- Example use cases
- Possible implementation approaches

### 🎮 Share Game Prompts

Found a cool prompt that generates an awesome game? Share it!
- [Open an issue using the "New Game Prompt" template](https://github.com/sausi-7/promptplay/issues/new?template=new_game_prompt.md)
- Include the prompt text
- Describe what the game does
- Add any tips for tweaking it

### 📝 Improve Documentation

Documentation improvements are always welcome:
- Fix typos or unclear sections
- Add examples
- Improve API documentation
- Add tutorials or guides

### 💻 Write Code

Whether you're fixing bugs or adding features, here's how to get started:

## Development Setup

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/promptplay.git
   cd promptplay
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   ```bash
   cp .env.example .env
   # Edit .env with your ANTHROPIC_API_KEY
   ```

5. **Test your setup**
   ```bash
   python agent.py
   ```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `fix/bug-description` for bug fixes
- `feature/feature-name` for new features
- `docs/what-changed` for documentation

### Code Style

- Use clear, descriptive variable names
- Keep functions focused and modular
- Follow PEP 8 conventions
- Add docstrings for public functions

### Commit Messages

Write clear commit messages:
```
Brief summary (50 chars max)

Longer explanation if needed. Explain *why* the change was made,
not just what changed. Reference issues with #123.
```

### Testing

Before submitting, run the full test suite:

```bash
pip install pytest pytest-mock pytest-asyncio
pytest tests/test_agent.py -v
```

All 5 tests should pass. No API key is required — all Claude API calls are mocked.

## Submitting a Pull Request

1. **Push your branch** to your fork
2. **Open a PR** on the main repository
3. **Fill out the PR template** with:
   - What changed and why
   - How to test it
   - Any related issues (closes #123)
4. **Respond to feedback** from reviewers

## Pull Request Guidelines

- Keep PRs focused (one feature or fix per PR)
- Update the CHANGELOG.md with your changes
- Add tests if you're adding new functionality
- Ensure your code doesn't break existing functionality

## Reviewer Expectations

PRs will be reviewed for:
- ✓ Correctness
- ✓ Code clarity
- ✓ Alignment with project goals
- ✓ Documentation and comments where needed

## Questions?

- Check [existing issues](https://github.com/sausi-7/promptplay/issues) for similar questions
- Ask in a new issue—don't worry about bothering us!
- Start discussions on the repo

## Recognition

Contributors are recognized in:
- The README (once significant contribution)
- Release notes for features
- GitHub's contributor list

Thank you for making PrompttoPlay better! 🚀
