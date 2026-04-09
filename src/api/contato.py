from fastapi import APIRouter
from schemas.contato import ContatoInput
from services.contato import ContatoService

router = APIRouter(prefix="/contato", tags=["Contato"])

@router.post("")
def enviar_mensagem(dados: ContatoInput):
    return ContatoService().enviar(dados)