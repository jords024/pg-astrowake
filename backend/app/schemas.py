from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re

class LeadCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)
    telefone: str = Field(..., min_length=10, max_length=20)
    origem: Optional[str] = "pg-astrowake"
    url: Optional[str] = None
    ts: Optional[str] = None

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("O nome deve ter pelo menos 2 caracteres.")
        return v

    @field_validator('telefone')
    @classmethod
    def validar_telefone(cls, v: str) -> str:
        digitos = re.sub(r'\D', '', v)
        if len(digitos) < 10:
            raise ValueError("Telefone invalido. Deve conter DDD + numero.")
        return digitos

class LeadUpdate(BaseModel):
    status: Optional[str] = None
    chamado: Optional[bool] = None

    @field_validator('status')
    @classmethod
    def validar_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.lower().strip()
            status_permitidos = ["novo", "chamado", "comprou", "desistiu"]
            if v not in status_permitidos:
                raise ValueError(f"Status invalido. Escolha entre: {', '.join(status_permitidos)}")
        return v

class LeadResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    origem: Optional[str]
    url: Optional[str]
    status: str
    chamado: bool
    created_at: datetime

    class Config:
        from_attributes = True