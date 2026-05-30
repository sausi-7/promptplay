from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import generate_game_html

app = FastAPI(title="PromptPlay")


# Request model - tells FastAPI what data to expect
class GameRequest(BaseModel):
    game_idea: str


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
