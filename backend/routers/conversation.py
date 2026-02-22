from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.conversation import Conversation
from models.report import Report
from schemas.schemas import CreateConversation, ConversationOut

router = APIRouter(prefix="/conversation", tags=["Conversations"])


@router.post("/", response_model=ConversationOut)
def create_conversation(body: CreateConversation, db: Session = Depends(get_db)):
    conversation = Conversation(title=body.title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


@router.get("/{conversation_id}", response_model=ConversationOut)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


# ← NEW: Get all reports for a conversation
@router.get("/{conversation_id}/reports")
def get_reports(conversation_id: int, db: Session = Depends(get_db)):
    """Fetch all uploaded report images for a conversation."""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    reports = (
        db.query(Report)
        .filter(Report.conversation_id == conversation_id)
        .order_by(Report.created_at.desc())
        .all()
    )

    return [
        {
            "id": r.id,
            "original_filename": r.original_filename,
            "file_url": f"/uploads/{r.stored_filename}",
            "mime_type": r.mime_type,
            "file_size": r.file_size,
            "uploaded_at": r.created_at,
        }
        for r in reports
    ]