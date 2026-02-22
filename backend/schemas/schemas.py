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

class ReportOut(BaseModel):             
    id: int
    original_filename: str
    stored_filename: str
    file_url: str                       
    mime_type: str
    file_size: int
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

class ConversationWithReportsOut(BaseModel):   
    id: int
    title: str
    created_at: datetime
    messages: List[MessageOut] = []
    reports: List[ReportOut] = []

    class Config:
        from_attributes = True