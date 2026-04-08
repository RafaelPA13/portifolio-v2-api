from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.base import get_db
from schemas.experiencias import ExperienciaInput, ExperienciaOutput
from services.experiencias import ExperienciaService
from core.security import get_admin_atual

router = APIRouter(prefix="/experiencias", tags=["Experiências"])

@router.post("", status_code=201, responses={
    201: {"description": "Experiência Adicionada"},
    400: {"description": "Os campos não podem estar vazios"},
    401: {"description": "Credenciais inválidas"},
    409: {"description": "Experiência já registrada"},
})
def criar(dados: ExperienciaInput, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    return ExperienciaService(db).criar(dados)

@router.get("", response_model=list[ExperienciaOutput], responses={
    400: {"description": "Nenhum Registro Encontrado"},
})
def listar(db: Session = Depends(get_db)):
    return ExperienciaService(db).listar()

@router.get("/{id}", response_model=ExperienciaOutput, responses={
    400: {"description": "Nenhum Registro Encontrado"},
    401: {"description": "Credenciais inválidas"},
})
def buscar(id: int, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    return ExperienciaService(db).buscar(id)

@router.put("/{id}", response_model=ExperienciaOutput, responses={
    400: {"description": "Os campos não podem estar vazios"},
    401: {"description": "Credenciais inválidas"},
    409: {"description": "Experiência já registrada"},
})
def atualizar(id: int, dados: ExperienciaInput, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    return ExperienciaService(db).atualizar(id, dados)

@router.delete("/{id}", status_code=204, responses={
    401: {"description": "Credenciais inválidas"},
})
def remover(id: int, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    ExperienciaService(db).remover(id)