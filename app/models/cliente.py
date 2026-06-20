from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ClienteCreate(BaseModel):
    """Dados recebidos para CRIAR um novo cliente (POST)."""
    nome: str = Field(..., min_length=2, max_length=120, examples=["Maria Silva"])
    email: EmailStr = Field(..., examples=["maria.silva@email.com"])
    telefone: str = Field(..., min_length=8, max_length=20, examples=["(47) 99999-0000"])
    cep: Optional[str] = Field(None, examples=["89010-000"])
    cidade: Optional[str] = Field(None, examples=["Blumenau"])
    estado: Optional[str] = Field(None, examples=["SC"])
    ativo: bool = True


class ClienteUpdate(BaseModel):
    """Dados recebidos para ATUALIZAR um cliente (PUT). Todos os campos são opcionais."""
    nome: Optional[str] = Field(None, min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, min_length=8, max_length=20)
    cep: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    ativo: Optional[bool] = None


class ClienteOut(BaseModel):
    """Formato de cliente retornado nas respostas da API."""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id")
    nome: str
    email: str
    telefone: str
    cep: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    ativo: bool = True
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None


class StatusResponse(BaseModel):
    """Resposta padrão de status para operações de escrita (POST/PUT/DELETE)."""
    sucesso: bool
    mensagem: str
    dados: Optional[dict] = None
