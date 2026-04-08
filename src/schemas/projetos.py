from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from schemas.tecnologias import TecnologiaOutput

class RepositorioOutput(BaseModel):
    id: int
    link: str
    tipo: str

    model_config = {"from_attributes": True}

class ProjetoInput(BaseModel):
    nome: str
    resumo: str
    descricao: str
    link_projeto: Optional[str] = None
    tecnologias: str
    link_unico: Optional[str] = None
    link_backend: Optional[str] = None
    link_frontend: Optional[str] = None

class ProjetoOutput(BaseModel):
    id: int
    nome: str
    resumo: str
    descricao: str
    imagem: Optional[str]
    link_projeto: Optional[str]
    criado_em: date
    tecnologias: List[TecnologiaOutput]
    repositorios: List[RepositorioOutput]

    model_config = {"from_attributes": True}