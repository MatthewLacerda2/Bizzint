import uuid
from datetime import datetime
from fastapi.models.base import Base
from sqlalchemy import Column, String, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID

class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cnpj = Column(String, nullable=False, unique=True)
    razao_social = Column(String, nullable=False)
    nome_fantasia = Column(String, nullable=True)

    situacao_cadastral = Column(String, nullable=True)
    data_inicio_atividade = Column(DateTime, nullable=True)
    cnae_principal = Column(String, nullable=True)
    natureza_juridica = Column(String, nullable=True)

    bairro = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    email = Column(String, nullable=True)
    telefone_1 = Column(String, nullable=True)
    telefone_2 = Column(String, nullable=True)
    capital_social = Column(Numeric(precision=15, scale=2), nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    last_updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)