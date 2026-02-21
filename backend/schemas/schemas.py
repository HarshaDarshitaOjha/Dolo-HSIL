from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Request Schemas

class CreateConversation(BaseModel):
    title: Optional[str] = "New Conversation"

class SendMessage(BaseModel):
    message: str

# Response Schemas

class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: List[MessageOut] = []

    class Config:
        from_attributes = True