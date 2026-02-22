from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class Report(Base):
    __tablename__ = "Reports"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    original_filename = Column(String)           # e.g. "blood_test.jpg"
    stored_filename = Column(String, unique=True) # e.g. "1708123456_blood_test.jpg"
    file_path = Column(Text)                      # e.g. "uploads/1708123456_blood_test.jpg"
    mime_type = Column(String)                    # e.g. "image/jpeg"
    file_size = Column(Integer)                   # bytes
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    conversation = relationship("Conversation", back_populates="reports")