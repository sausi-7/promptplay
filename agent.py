import asyncio
import argparse
import re
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

load_dotenv()


def htmlParser(result: str) -> str:
    """Extract HTML from markdown code blocks, prioritizing html-tagged blocks."""
    # First try to find an html-tagged code block
    match = re.search(r'```html\s*(.*?)\s*```', result, re.DOTALL)
    if match:
        return match.group(1).strip()

    # If no html block, try any code block (for backwards compatibility)
    match = re.search(r'```\s*(.*?)\s*```', result, re.DOTALL)
    if match:
        content = match.group(1).strip()
        # Skip if it's a non-HTML code block (bash, python, etc.)
        if not content.startswith(('bash', 'sh', 'python', 'js\n', 'javascript\n')):
            return content

    return result.strip()


def build_prompt(game_idea: str) -> str:
    """Wrap a raw game idea with strict instructions so the model returns only HTML."""
    return (
        f"Create a complete, playable, single-file HTML/CSS/JavaScript game.\n\n"
        f"Game Idea: {game_idea}\n\n"
        f"Requirements:\n"
        f"1. Embed ALL code (HTML, CSS, JavaScript) in a single file\n"
        f"2. Use HTML5 doctype and semantic structure\n"
        f"3. Make it fully playable - no broken features\n"
        f"4. Include clear instructions or tutorial for the player\n"
        f"5. Add a reset/restart button\n"
        f"6. Make it responsive - works on desktop and mobile\n"
        f"7. Use keyboard controls or mouse clicks (clearly labeled)\n"
        f"8. Include visual feedback (colors, animations, sounds if appropriate)\n"
        f"9. Add a score/level system if relevant to the game type\n\n"
        f"Output: Return ONLY the complete HTML code wrapped in ```html code blocks.\n"
        f"No explanations, no markdown text before/after, no tool usage."
    )


def _progress_bar(percent: int) -> str:
    filled = max(0, min(10, round(percent / 10)))
    return "[" + "█" * filled + "░" * (10 - filled) + "]"


def _message_text(message) -> str:
    """Best-effort text extraction across Claude Agent SDK stream message shapes."""
    parts = []
    content = getattr(message, "content", None)
    if isinstance(content, str):
        parts.append(content)
    elif isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and isinstance(block.get("text"), str):
                parts.append(block["text"])
            elif hasattr(block, "text") and isinstance(block.text, str):
                parts.append(block.text)

    for attr in ("text", "delta", "result"):
        value = getattr(message, attr, None)
        if isinstance(value, str):
            parts.append(value)

    return "".join(parts)


class StreamReporter:
    """Small stdout reporter for CLI streaming without coupling to SDK internals."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.message_count = 0
        self.started_code = False

    def start(self):
        print("Generating game...", flush=True)
        self.progress(10, "Connecting to Claude")

    def progress(self, percent: int, label: str):
        print(f"{_progress_bar(percent)} {percent}% - {label}", flush=True)

    def observe(self, message):
        self.message_count += 1
        if self.message_count == 1:
            self.progress(30, "Planning game structure")
        elif self.message_count == 2:
            self.progress(50, "Writing game logic")

        if self.verbose:
            print(f"\n[stream] message {self.message_count}: {type(message).__name__}", flush=True)

        text = _message_text(message)
        if not text:
            return

        if not self.started_code:
            self.started_code = True
            print("\n--- generated output stream ---", flush=True)
        print(text, end="" if text.endswith("\n") else "\n", flush=True)

    def complete(self):
        self.progress(100, "Complete!")


async def generate_game_html(game_idea: str, stream: bool = False, verbose: bool = False) -> str:
    """
    Generate game HTML from a game idea.
    Wraps the idea with strict instructions and returns the generated HTML code.
    """
    html_content = None
    prompt = build_prompt(game_idea)
    reporter = StreamReporter(verbose=verbose) if stream else None
    if reporter:
        reporter.start()

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model="claude-haiku-4-5-20251001",
            allowed_tools=[],
            effort="low",
        ),
    ):
        if reporter:
            reporter.observe(message)
        if hasattr(message, "result"):
            html_content = htmlParser(message.result)

    if html_content is None:
        raise Exception("Failed to generate game HTML")

    if reporter:
        reporter.complete()

    return html_content


async def main():
    """Main function for CLI usage."""
    parser = argparse.ArgumentParser(description="Generate a playable HTML game from a prompt.")
    parser.add_argument(
        "game_idea",
        nargs="*",
        help="Game idea to generate. Uses a tic-tac-toe example when omitted.",
    )
    parser.add_argument("--output", "-o", default="output.html", help="Output HTML file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed stream logs")
    args = parser.parse_args()

    game_idea = (
        " ".join(args.game_idea).strip()
        or "A tic tac toe game where the player is X and plays against an AI opponent (O) that uses the minimax algorithm for intelligent moves."
    )
    html = await generate_game_html(game_idea, stream=True, verbose=args.verbose)

    with open(args.output, "w") as output_file:
        output_file.write(html)
    print(f"✓ Game saved to {args.output}")


if __name__ == "__main__":
    asyncio.run(main())
