import asyncio
import re
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

load_dotenv()


async def main():
    async for message in query(
        prompt="Write code for a snake game and give me one single index.html code",
        options=ClaudeAgentOptions(
            model="claude-haiku-4-5-20251001",
            allowed_tools=["Bash", "Glob"],
            effort="low",
        ),
    ):
        
        if hasattr(message, "result"):
            html = htmlParser(message.result)
            with open("output.html", "w") as f:
                f.write(html)
            print("✓ Game saved to output.html")

def htmlParser(result: str) -> str:
    """Extract HTML from markdown code blocks."""
    match = re.search(r'```(?:html)?\s*(.*?)\s*```', result, re.DOTALL)
    if match:
        return match.group(1).strip()
    return result.strip()



asyncio.run(main())