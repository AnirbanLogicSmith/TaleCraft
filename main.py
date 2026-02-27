from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from google import genai
from google.genai import types
import os
import json
import re

app = FastAPI(title="TaleCraft", description="AI-powered interactive story generator")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Models ────────────────────────────────────────────────────────────────────

class StartStoryRequest(BaseModel):
    genre: str
    premise: str


class ContinueStoryRequest(BaseModel):
    genre: str
    history: list[dict]   # [{"segment": "...", "choice": "..."}]
    choice: str


class StorySegment(BaseModel):
    segment: str
    choices: list[str]
    is_ending: bool = False


# ── Helpers ───────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are TaleCraft, a masterful interactive fiction author.
Your job is to write compelling, immersive story segments and offer meaningful choices.

Rules:
- Each segment should be 2-3 paragraphs (keep it concise).
- Always offer exactly 2 or 3 choices that are meaningfully different and interesting.
- Choices should be SHORT (max 10 words) yet evocative — they are buttons, not paragraphs.
- After 5-7 exchanges, you may end the story with a satisfying conclusion (set is_ending: true, choices: []).
- Match the tone and genre precisely.
- Never break the fourth wall.

CRITICAL: Respond ONLY with a single valid JSON object. No markdown, no code fences, no extra text before or after.
Use this exact shape:
{"segment": "<story text>", "choices": ["<choice 1>", "<choice 2>", "<choice 3 optional>"], "is_ending": false}
"""


def build_history_text(history: list[dict]) -> str:
    parts = []
    for h in history:
        parts.append(f"[STORY]: {h['segment']}")
        if h.get("choice"):
            parts.append(f"[PLAYER CHOSE]: {h['choice']}")
    return "\n\n".join(parts)


def extract_json(raw: str) -> dict:
    """Robustly extract JSON from the model response."""
    raw = raw.strip()

    # Strip markdown code fences
    if "```" in raw:
        raw = re.sub(r"```(?:json)?", "", raw).strip()

    # Try direct parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try to find the first { ... } block
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not extract valid JSON from response:\n{raw[:300]}")


def call_gemini(user_message: str) -> StorySegment:
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.9,
            max_output_tokens=2048,  # enough headroom for story + choices
        ),
    )
    data = extract_json(response.text)
    return StorySegment(**data)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("static/index.html")


@app.post("/api/start", response_model=StorySegment)
async def start_story(req: StartStoryRequest):
    """Start a brand new story."""
    try:
        user_message = (
            f"Genre: {req.genre}\n"
            f"Opening premise: {req.premise}\n\n"
            "Begin the story now. Set the scene, introduce intrigue, and end with choices. "
            "Remember: respond with JSON only."
        )
        return call_gemini(user_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/continue", response_model=StorySegment)
async def continue_story(req: ContinueStoryRequest):
    """Continue the story based on the player's choice."""
    try:
        history_text = build_history_text(req.history)
        user_message = (
            f"Genre: {req.genre}\n\n"
            f"Story so far:\n{history_text}\n\n"
            f"The player just chose: \"{req.choice}\"\n\n"
            "Continue the story based on this choice. "
            f"This is turn {len(req.history) + 1}. "
            "If 6+ turns have passed, consider a satisfying ending (is_ending: true). "
            "Remember: respond with JSON only."
        )
        return call_gemini(user_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
