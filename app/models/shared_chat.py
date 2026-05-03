import uuid
from datetime import datetime
from app.models.base import Base
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Column, String, DateTime, Integer, Text

class SharedChat(Base):
    __tablename__ = "shared_chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), nullable=False, unique=False)
    order = Column(Integer, nullable=False)
    user_message = Column(Text, nullable=False)
    assistant_message = Column(Text, nullable=True)
    plots = Column(JSONB, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)