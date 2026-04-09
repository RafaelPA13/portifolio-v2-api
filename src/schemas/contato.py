from pydantic import BaseModel
from typing import Optional

class ContatoInput(BaseModel):
    nome:     str
    email:    str
    assunto:  Optional[str] = None
    mensagem: str