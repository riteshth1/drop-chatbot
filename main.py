from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
import os
from database import init_db, save_message, get_conversation, search_by_topic, get_all_sessions
from claude_client import get_chat_response, detect_topic, get_visual_context
from dotenv import load_dotenv
from fastapi.responses import FileResponse

load_dotenv()
init_db()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

@app.post("/chat")
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    topic = detect_topic(req.message)
    past_context = search_by_topic(topic)
    history = get_conversation(session_id)
    conversation_history = [{"role": m["role"], "content": m["content"]} for m in history]

    response = get_chat_response(req.message, conversation_history, past_context)
    
    visuals = get_visual_context(req.message)

    save_message(session_id, "user", req.message, topic)
    save_message(session_id, "assistant", response, topic)

    return {
        "session_id": session_id,
        "response": response,
        "topic": topic,
        "images": visuals["images"] if visuals else [],
        "link": visuals["link"] if visuals else None
    }

@app.get("/conversations/{session_id}")
async def get_history(session_id: str):
    return get_conversation(session_id)

@app.get("/conversations/topic/{topic}")
async def get_by_topic(topic: str):
    return search_by_topic(topic)

@app.get("/sessions")
async def get_sessions():
    return get_all_sessions()