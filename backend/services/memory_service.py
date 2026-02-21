from sqlalchemy.orm import Session
from models.message import Message
from utils.prompts import SYSTEM_PROMPT, MEMORY_PROMPT

MAX_CONTEXT_MESSAGES = 10


def build_context(db: Session, conversation_id: int, new_user_message: str = None):
    """
    Reconstructs the conversation context for OpenAI.
    Fetches last N messages, prepends system + memory prompts.
    Returns a messages array ready for the OpenAI API.
    """
    # Fetch last N messages ordered by creation time
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .limit(MAX_CONTEXT_MESSAGES)
        .all()
    )

    # Build the messages array
    context = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    # Add memory prompt only if there are previous messages
    if len(messages) > 0:
        context.append({"role": "system", "content": MEMORY_PROMPT})

    # Add previous messages
    for msg in messages:
        context.append({"role": msg.role, "content": msg.content})

    # Add new user message if provided
    if new_user_message:
        context.append({"role": "user", "content": new_user_message})

    return context


def store_message(db: Session, conversation_id: int, role: str, content: str):
    """Store a message in the database."""
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message