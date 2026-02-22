import os
import time
import base64
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from models.conversation import Conversation
from models.report import Report
from schemas.schemas import SendMessage
from services.memory_service import build_context, store_message
from services.ai_service import get_ai_response, get_ai_response_with_image

router = APIRouter(tags=["AI Analysis"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --- Text Chat Endpoint ---

@router.post("/chat/{conversation_id}")
def chat(conversation_id: int, body: SendMessage, db: Session = Depends(get_db)):
    """Text-based chat with AI. Maintains conversation memory."""

    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    store_message(db, conversation_id, "user", body.message)
    context = build_context(db, conversation_id)
    result = get_ai_response(context)

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])

    store_message(db, conversation_id, "assistant", result["raw"])

    return {
        "conversation_id": conversation_id,
        "response": result["data"] if result["data"] else result["raw"],
    }


# --- Image Analysis Endpoint (NOW WITH STORAGE) ---

ALLOWED_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/webp"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@router.post("/analyze-report/{conversation_id}")
async def analyze_report(
    conversation_id: int,
    file: UploadFile = File(...),
    message: str = Form(default="Analyze this medical report in detail."),
    db: Session = Depends(get_db),
):
    """Upload a medical report image for AI analysis. Image is STORED for future reference."""

    # 1. Verify conversation exists
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 2. Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail={"error": "Invalid file type", "allowed": ALLOWED_TYPES},
        )

    # 3. Read and validate file size
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail={"error": "File too large", "max_size": "5MB"},
        )

    # 4. Generate a unique filename and SAVE TO DISK
    timestamp = int(time.time())
    safe_name = file.filename.replace(" ", "_")
    stored_filename = f"{timestamp}_{safe_name}"
    file_path = os.path.join(UPLOAD_DIR, stored_filename)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # 5. Save report metadata to the DATABASE
    report = Report(
        conversation_id=conversation_id,
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=file_path,
        mime_type=file.content_type,
        file_size=len(file_bytes),
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    # 6. Convert to base64 for AI (same as before)
    base64_image = base64.b64encode(file_bytes).decode("utf-8")

    # 7. Store user message
    store_message(
        db, conversation_id, "user",
        f"[Image uploaded: {file.filename} | Report ID: {report.id}] {message}"
    )

    # 8. Build context and send to Gemini
    context = build_context(db, conversation_id)
    result = get_ai_response_with_image(context, base64_image, file.content_type)

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])

    # 9. Store assistant reply
    store_message(db, conversation_id, "assistant", result["raw"])

    return {
        "conversation_id": conversation_id,
        "report_id": report.id,
        "filename": file.filename,
        "file_url": f"/uploads/{stored_filename}",
        "response": result["data"] if result["data"] else result["raw"],
    }