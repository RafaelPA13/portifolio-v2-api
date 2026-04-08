from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.base import get_db
from schemas.tecnologias import TecnologiaInput, TecnologiaOutput
from services.tecnologias import TecnologiaService
from core.security import get_admin_atual

router = APIRouter(prefix="/tecnologias", tags=["Tecnologias"])

@router.post("", status_code=201, responses={
    201: {"description": "Tecnologia Adicionada"},
    400: {"description": "Os campos não podem estar vazios"},
    401: {"description": "Credenciais inválidas"},
    409: {"description": "Tecnologia já registrada"},
})
def criar(dados: TecnologiaInput, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    return TecnologiaService(db).criar(dados)

@router.get("", response_model=list[TecnologiaOutput], responses={
    400: {"description": "Nenhum Registro Encontrado"},
})
def listar(db: Session = Depends(get_db)):
    return TecnologiaService(db).listar()

@router.get("/{id}", response_model=TecnologiaOutput, responses={
    400: {"description": "Nenhum Registro Encontrado"},
    401: {"description": "Credenciais inválidas"},
})
def buscar(id: int, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    return TecnologiaService(db).buscar(id)

@router.put("/{id}", response_model=TecnologiaOutput, responses={
    400: {"description": "Os campos não podem estar vazios"},
    401: {"description": "Credenciais inválidas"},
    409: {"description": "Tecnologia já registrada"},
})
def atualizar(id: int, dados: TecnologiaInput, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    return TecnologiaService(db).atualizar(id, dados)

@router.delete("/{id}", status_code=204, responses={
    401: {"description": "Credenciais inválidas"},
})
def remover(id: int, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    TecnologiaService(db).remover(id)