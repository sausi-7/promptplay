import asyncio
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
        f"Write a complete, single-file HTML/CSS/JavaScript game based on this idea: {game_idea}. "
        "Put all HTML, CSS, and JavaScript in one file. "
        "Return ONLY the HTML code wrapped in ```html code blocks, with no other text, "
        "no explanations, and no tool usage."
    )


async def generate_game_html(game_idea: str) -> str:
    """
    Generate game HTML from a game idea.
    Wraps the idea with strict instructions and returns the generated HTML code.
    """
    html_content = None
    prompt = build_prompt(game_idea)

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model="claude-haiku-4-5-20251001",
            allowed_tools=[],
            effort="low",
        ),
    ):
        if hasattr(message, "result"):
            html_content = htmlParser(message.result)

    if html_content is None:
        raise Exception("Failed to generate game HTML")

    return html_content


async def main():
    """Main function for CLI usage."""
    game_idea = "A tic tac toe game where the player is X and plays against an AI opponent (O) that uses the minimax algorithm for intelligent moves."
    html = await generate_game_html(game_idea)

    with open("output.html", "w") as output_file:
        output_file.write(html)
    print("✓ Game saved to output.html")


if __name__ == "__main__":
    asyncio.run(main())
