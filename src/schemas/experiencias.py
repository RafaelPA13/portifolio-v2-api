from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from schemas.tecnologias import TecnologiaOutput

class ExperienciaInput(BaseModel):
    cargo: str
    empresa: str
    descricao: str
    dt_inicio: date
    dt_fim: Optional[date] = None
    atual: bool = False
    tecnologias: str


class ExperienciaOutput(BaseModel):
    id: int
    cargo: str
    empresa: str
    descricao: str
    dt_inicio: date
    dt_fim: Optional[date]
    atual: bool
    tecnologias: List[TecnologiaOutput]

    model_config = {"from_attributes": True}