from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from schemas.tecnologias import TecnologiaOutput

class CertificadoInput(BaseModel):
    nome: str
    instituicao: str
    carga_horaria: Optional[int] = None
    link: str
    dt_conclusao: date
    tecnologias: str

class CertificadoOutput(BaseModel):
    id: int
    nome: str
    instituicao: str
    carga_horaria: Optional[int]
    link: str
    dt_conclusao: date
    criado_em: date
    tecnologias: List[TecnologiaOutput]

    model_config = {"from_attributes": True}