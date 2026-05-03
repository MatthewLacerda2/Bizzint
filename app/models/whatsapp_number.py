import uuid
from datetime import datetime
from app.models.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Boolean

class WhatsappNumber(Base):
    __tablename__ = "whatsapp_number"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, nullable=False)
    is_on_whatsapp = Column(Boolean, nullable=False)
    is_business = Column(Boolean, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    last_updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)