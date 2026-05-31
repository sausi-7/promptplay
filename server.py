import asyncio
import uuid
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import generate_game_html
from conversation_agent import (
    ask_clarifications,
    generate_game,
    refine_game,
    ConversationMemory,
    build_clarification_prompt,
    htmlParser,
)
from claude_agent_sdk import query, ClaudeAgentOptions

app = FastAPI(title="PromptPlay")

# Store conversation state in memory
conversations = {}


# Request models
class GameRequest(BaseModel):
    game_idea: str


class ConversationStartRequest(BaseModel):
    game_idea: str


class ConversationAnswerRequest(BaseModel):
    session_id: str
    answers: str


class ConversationRefineRequest(BaseModel):
    session_id: str
    refinement: str


# Serve the index.html file when user visits http://localhost:8000/
@app.get("/")
async def get_home():
    return FileResponse("index.html")


# Handle POST requests to /generate
@app.post("/generate")
async def generate_game(request: GameRequest):
    """
    Receives a game idea, generates the game, saves it to output.html,
    and reports whether generation succeeded.
    """
    try:
        html = await generate_game_html(request.game_idea)
        with open("output.html", "w") as f:
            f.write(html)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Serve the most recently generated game
@app.get("/game")
async def get_game():
    return FileResponse("output.html", headers={"Cache-Control": "no-store"})


# Conversation endpoints
@app.post("/conversation/start")
async def start_conversation(request: ConversationStartRequest):
    """
    Start a new conversation. Get clarifying questions from Claude.
    """
    try:
        session_id = str(uuid.uuid4())
        game_idea = request.game_idea

        # Build prompt and get questions
        prompt = build_clarification_prompt(game_idea)
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

        # Store conversation state
        conversations[session_id] = {
            "game_idea": game_idea,
            "clarifications": {},
            "questions": questions,
            "memory": ConversationMemory(session_id),
        }
        conversations[session_id]["memory"].set_game_idea(game_idea)

        return {
            "success": True,
            "session_id": session_id,
            "questions": questions,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/conversation/answer")
async def answer_questions(request: ConversationAnswerRequest):
    """
    Receive user's answers and generate the game.
    """
    try:
        session_id = request.session_id
        answers = request.answers

        if session_id not in conversations:
            return {"success": False, "error": "Session not found"}

        conv = conversations[session_id]
        conv["clarifications"]["user_answers"] = answers
        conv["memory"].add_clarification("user_answers", answers)

        # Generate game with answers
        game_idea = conv["game_idea"]
        clarifications = conv["clarifications"]

        html_content = ""
        async for message in query(
            prompt=(
                f"Create a complete, playable, single-file HTML/CSS/JavaScript game.\n\n"
                f"Game Idea: {game_idea}\n\n"
                f"User Specifications: {answers}\n\n"
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
            ),
            options=ClaudeAgentOptions(
                model="claude-haiku-4-5-20251001",
                allowed_tools=[],
                effort="low",
            ),
        ):
            if hasattr(message, "result"):
                html_content = htmlParser(message.result)

        if not html_content:
            return {"success": False, "error": "Failed to generate game"}

        # Save game
        with open("output.html", "w") as f:
            f.write(html_content)

        conv["memory"].add_generation("", html_content)
        conv["html"] = html_content

        return {"success": True, "message": "Game generated successfully"}

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/conversation/refine")
async def refine_conversation(request: ConversationRefineRequest):
    """
    Refine the game based on user feedback.
    """
    try:
        session_id = request.session_id
        refinement = request.refinement

        if session_id not in conversations:
            return {"success": False, "error": "Session not found"}

        conv = conversations[session_id]
        game_idea = conv["game_idea"]
        clarifications = conv["clarifications"]

        # Generate refined game
        html_content = ""
        async for message in query(
            prompt=(
                f"Refine this game based on feedback: {refinement}\n\n"
                f"Original Game Idea: {game_idea}\n"
                f"User Specifications: {clarifications.get('user_answers', '')}\n\n"
                f"Create an improved version that addresses the feedback.\n"
                f"Return ONLY the complete HTML code wrapped in ```html code blocks."
            ),
            options=ClaudeAgentOptions(
                model="claude-haiku-4-5-20251001",
                allowed_tools=[],
                effort="low",
            ),
        ):
            if hasattr(message, "result"):
                html_content = htmlParser(message.result)

        if not html_content:
            return {"success": False, "error": "Failed to refine game"}

        # Save refined game
        with open("output.html", "w") as f:
            f.write(html_content)

        conv["memory"].add_refinement(refinement, html_content)
        conv["html"] = html_content

        return {"success": True, "message": "Game refined successfully"}

    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
