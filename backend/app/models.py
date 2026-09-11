from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    telefone = Column(String(50), nullable=False, index=True)
    origem = Column(String(100), nullable=True, default="pg-astrowake")
    url = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default="novo", index=True)
    chamado = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)