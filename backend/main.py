from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import engine, Base
from routers import conversation, analyze

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dolo - Medical Report AI Analyzer",
    description="AI-powered medical report analysis backend",
    version="1.0.0",
)

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Global Error Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)},
    )


# --- Health Check ---
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Dolo AI Backend", "version": "1.0.0"}


# --- Register Routers ---
app.include_router(conversation.router)
app.include_router(analyze.router)