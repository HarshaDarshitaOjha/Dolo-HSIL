from fastapi import FastAPI, Depends
from database import Base, engine, get_db
from routers import conversation, analyze
from sqlalchemy.orm import Session
from services.memory_service import build_context, store_message
from config import GEMINI_API_KEY

# Create all tables
Base.metadata.create_all(bind = engine)

app = FastAPI(title = "Dolo - Medical Report AI Analyzer")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Dolo backend is running"}

# Register routers

app.include_router(conversation.router)
app.include_router(analyze.router)

@app.get("/debug-key")
def debug_key():
    return {"key_starts_with": GEMINI_API_KEY[:10] if GEMINI_API_KEY else "NONE"}