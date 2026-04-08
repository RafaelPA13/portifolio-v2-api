from pydantic import BaseModel
from datetime import date
from typing import Optional

class TecnologiaInput(BaseModel):
    skill: str

class TecnologiaOutput(BaseModel):
    id: int
    skill: str
    dt_criacao: date
    dt_atualizacao: Optional[date]

    model_config = {"from_attributes": True}