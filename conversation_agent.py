import asyncio
import json
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

load_dotenv()


class ConversationMemory:
    """Store and manage conversation history."""

    def __init__(self, game_id: str = None):
        self.game_id = game_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.memory_file = Path(f"games/{self.game_id}_memory.json")
        self.memory_file.parent.mkdir(exist_ok=True)

        self.data = {
            "game_id": self.game_id,
            "created_at": datetime.now().isoformat(),
            "game_idea": None,
            "clarifications": {},
            "generations": [],
            "refinements": [],
        }

    def set_game_idea(self, idea: str):
        self.data["game_idea"] = idea
        self.save()

    def add_clarification(self, key: str, value: str):
        self.data["clarifications"][key] = value
        self.save()

    def add_generation(self, prompt: str, html: str):
        gen = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "html_size": len(html),
            "html_file": f"output_{len(self.data['generations'])}.html"
        }
        self.data["generations"].append(gen)
        self.save()

    def add_refinement(self, request: str, html: str):
        ref = {
            "timestamp": datetime.now().isoformat(),
            "request": request,
            "html_size": len(html),
            "html_file": f"output_refined_{len(self.data['refinements'])}.html"
        }
        self.data["refinements"].append(ref)
        self.save()

    def save(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_conversation_context(self) -> str:
        """Build context string from memory for Claude."""
        lines = [f"Game Idea: {self.data['game_idea']}"]

        if self.data["clarifications"]:
            lines.append("\nUser Specifications:")
            for key, val in self.data["clarifications"].items():
                lines.append(f"  - {key}: {val}")

        return "\n".join(lines)


def htmlParser(result: str) -> str:
    """Extract HTML from Claude's response."""
    match = re.search(r'```html\s*(.*?)\s*```', result, re.DOTALL)
    if match:
        return match.group(1).strip()

    match = re.search(r'```\s*(.*?)\s*```', result, re.DOTALL)
    if match:
        content = match.group(1).strip()
        if not content.startswith(('bash', 'sh', 'python', 'js\n', 'javascript\n')):
            return content

    return result.strip()


def build_clarification_prompt(game_idea: str) -> str:
    """Build prompt for Claude to ask clarifying questions."""
    return (
        f"A user wants to create a game with this idea: {game_idea}\n\n"
        f"Ask 3-4 clarifying questions to better understand their vision only when needed. "
        f"Ask about:\n"
        f"- Difficulty/complexity level\n"
        f"- Key gameplay mechanics or features\n"
        f"- Target audience (casual player, hardcore gamer, kids, etc.)\n"
        f"- Any specific visual style or theme\n\n"
        f"Be friendly and conversational. Keep it brief."
    )


def build_generation_prompt(game_idea: str, clarifications: dict) -> str:
    """Build prompt for final game generation."""
    context = f"Game Idea: {game_idea}\n\nUser Specifications:\n"
    for key, val in clarifications.items():
        context += f"  - {key}: {val}\n"

    return (
        f"Create a complete, playable, single-file HTML/CSS/JavaScript game.\n\n"
        f"{context}\n"
        f"Requirements:\n"
        f"1. Embed ALL code (HTML, CSS, JavaScript) in a single file\n"
        f"2. Use HTML5 doctype and semantic structure\n"
        f"3. Make it fully playable - no broken features\n"
        f"4. Include clear instructions or tutorial for the player\n"
        f"5. Add a reset/restart button\n"
        f"6. Keep total file size under 100KB\n"
        f"7. Make it responsive - works on desktop and mobile\n"
        f"8. Use keyboard controls or mouse clicks (clearly labeled)\n"
        f"9. Include visual feedback (colors, animations, sounds if appropriate)\n"
        f"10. Match the specifications above as closely as possible\n\n"
        f"Output: Return ONLY the complete HTML code wrapped in ```html code blocks.\n"
        f"No explanations, no markdown text before/after, no tool usage."
    )


def build_refinement_prompt(game_idea: str, clarifications: dict, refinement_request: str) -> str:
    """Build prompt for refining an existing game."""
    context = f"Game Idea: {game_idea}\n\nOriginal Specifications:\n"
    for key, val in clarifications.items():
        context += f"  - {key}: {val}\n"

    return (
        f"Refine the game based on this feedback: {refinement_request}\n\n"
        f"{context}\n"
        f"Create an improved version that addresses the feedback while keeping all other aspects.\n"
        f"Return ONLY the complete HTML code wrapped in ```html code blocks."
    )


async def ask_clarifications(game_idea: str) -> dict:
    """Have Claude ask clarifying questions and collect answers."""
    print("\n🤔 Asking clarifying questions...\n")

    prompt = build_clarification_prompt(game_idea)

    # Get Claude's questions
    questions = ""
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model="claude-haiku-4-5-20251001",
            allowed_tools=[],
            effort="low",
        ),
    ):
        if hasattr(message, "result"):
            questions = message.result

    print(questions)
    print()

    # Collect answers
    clarifications = {}
    while True:
        user_input = input("Your answer (or 'done' to generate game): ").strip()
        if user_input.lower() == "done":
            break

        if user_input:
            key = f"clarification_{len(clarifications) + 1}"
            clarifications[key] = user_input

    return clarifications


async def generate_game(game_idea: str, clarifications: dict, memory: ConversationMemory) -> str:
    """Generate the game HTML based on idea and clarifications."""
    print("\n⏳ Generating your game...\n")

    prompt = build_generation_prompt(game_idea, clarifications)
    memory.add_clarification("consolidated", json.dumps(clarifications))

    html_content = ""
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

    if not html_content:
        raise Exception("Failed to generate game HTML")

    memory.add_generation(prompt, html_content)
    return html_content


async def refine_game(game_idea: str, clarifications: dict, memory: ConversationMemory) -> str:
    """Refine the game based on user feedback."""
    refinement_request = input("\n💡 What should we change? ").strip()

    if not refinement_request:
        return None

    print("\n⏳ Refining your game...\n")

    prompt = build_refinement_prompt(game_idea, clarifications, refinement_request)

    html_content = ""
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

    if not html_content:
        raise Exception("Failed to refine game HTML")

    memory.add_refinement(refinement_request, html_content)
    return html_content


async def main():
    """Main conversational game generation flow."""
    print("\n🎮 PromptPlay - Conversational Game Generation\n")
    print("=" * 50)

    memory = ConversationMemory()

    # Step 1: Get game idea
    game_idea = input("\n📝 Describe your game idea: ").strip()
    if not game_idea:
        print("❌ Game idea is required")
        return

    memory.set_game_idea(game_idea)

    # Step 2: Ask clarifying questions
    clarifications = await ask_clarifications(game_idea)

    # Step 3: Generate initial game
    html = await generate_game(game_idea, clarifications, memory)

    with open("output.html", "w") as f:
        f.write(html)
    print("✅ Game saved to output.html\n")

    # Step 4: Allow refinements
    while True:
        response = input("Happy with the game? (yes/refine/quit): ").strip().lower()

        if response in ["yes", "quit", "q"]:
            print("\n✨ Game generation complete!")
            print(f"📁 Memory saved to {memory.memory_file}")
            break
        elif response == "refine":
            refined_html = await refine_game(game_idea, clarifications, memory)
            if refined_html:
                with open("output.html", "w") as f:
                    f.write(refined_html)
                print("✅ Game updated to output.html\n")
        else:
            print("❓ Please enter: yes, refine, or quit")


if __name__ == "__main__":
    asyncio.run(main())
