from fastapi import APIRouter
from schemas.contato import ContatoInput
from services.contato import ContatoService

router = APIRouter(prefix="/contato", tags=["Contato"])

@router.post("")
async def enviar_mensagem(dados: ContatoInput):
    return await ContatoService().enviar(dados)