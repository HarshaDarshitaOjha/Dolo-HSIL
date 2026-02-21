from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from models.conversation import Conversation
from schemas.schemas import SendMessage
from services.memory_service import build_context, store_message
from services.ai_service import get_ai_response, get_ai_response_with_image
import base64

router = APIRouter(tags=["AI Analysis"])
ALLOWED_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/webp"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@router.post("/chat/{conversation_id}")
def chat(conversation_id: int, body: SendMessage, db: Session = Depends(get_db)):
    """Text-based chat with AI. Maintains conversation memory."""

    # Verify conversation exists
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Store the user message
    store_message(db, conversation_id, "user", body.message)

    # Build context with all previous messages
    context = build_context(db, conversation_id)

    # Send to OpenAI
    result = get_ai_response(context)

    if not result["success"]:
        # map specific errors to HTTP status codes
        err_code = result.get("error")
        detail_msg = result.get("message", result.get("error"))
        if err_code == "quota_exceeded":
            # inform client of the quota problem
            raise HTTPException(
                status_code=429,
                detail=(
                    "OpenAI quota exceeded or rate limit hit. "
                    "Please check your plan/billing or try again later. "
                    f"({detail_msg})"
                ),
            )
        # generic 500 for other failures
        raise HTTPException(status_code=500, detail=detail_msg)

    # Store assistant reply
    store_message(db, conversation_id, "assistant", result["raw"])

    return {
        "conversation_id": conversation_id,
        "response": result["data"] if result["data"] else result["raw"],
    }

@router.post("/analyze-report/{conversation_id}")
async def analyze_report(
    conversation_id: int,
    file: UploadFile = File(...),
    message: str = Form(default="Analyze this medical report in detail."),
    db: Session = Depends(get_db),
):
    """Upload a medical report image for AI analysis."""

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
            detail={
                "error": "Invalid file type",
                "allowed": ALLOWED_TYPES,
                "received": file.content_type,
            },
        )

    # 3. Read and validate file size
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail={"error": "File too large", "max_size": "5MB"},
        )

    # 4. Convert to base64
    base64_image = base64.b64encode(file_bytes).decode("utf-8")

    # 5. Store user message
    store_message(db, conversation_id, "user", f"[Image uploaded: {file.filename}] {message}")

    # 6. Build context
    context = build_context(db, conversation_id)

    # 7. Send to OpenAI with image
    result = get_ai_response_with_image(context, base64_image, file.content_type)

    if not result["success"]:
        err_code = result.get("error")
        detail_msg = result.get("message", result.get("error"))
        if err_code == "quota_exceeded":
            raise HTTPException(
                status_code=429,
                detail=(
                    "OpenAI quota exceeded or rate limit hit. "
                    "Please check your plan/billing or try again later. "
                    f"({detail_msg})"
                ),
            )
        raise HTTPException(status_code=500, detail=detail_msg)

    # 8. Store assistant reply
    store_message(db, conversation_id, "assistant", result["raw"])

    return {
        "conversation_id": conversation_id,
        "filename": file.filename,
        "response": result["data"] if result["data"] else result["raw"],
    }