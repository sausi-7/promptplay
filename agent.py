import asyncio
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

load_dotenv()


async def main():
    async for message in query(
        prompt="Build me a snake game in single index.html",
        options=ClaudeAgentOptions(
            model="claude-haiku-4-5-20251001",
            allowed_tools=["Bash", "Glob"],
            effort="high",
        ),
    ):
        
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())