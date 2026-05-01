import uuid
from datetime import datetime
from fastapi.models.base import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

class Socio(Base):
    __tablename__ = "socios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    cnpj = Column(String, nullable=False)
    qualificacao = Column(String, nullable=False)
    data_entrada = Column(DateTime, nullable=False, default=datetime.now)
    identificador = Column(String, nullable=False)
    faixa_etaria = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    last_updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)