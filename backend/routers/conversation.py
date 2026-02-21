from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.conversation import Conversation
from models.message import Message
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