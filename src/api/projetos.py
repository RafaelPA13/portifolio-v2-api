from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from db.base import get_db
from schemas.projetos import ProjetoInput, ProjetoOutput
from services.projetos import ProjetoService
from core.security import get_admin_atual

router = APIRouter(prefix="/projetos", tags=["Projetos"])

@router.post("", status_code=201, responses={
    201: {"description": "Projeto Adicionado"},
    400: {"description": "Os campos não podem estar vazios"},
    401: {"description": "Credenciais inválidas"},
    409: {"description": "Projeto já registrado"},
})
def criar(
    nome: str = Form(...),
    resumo: str = Form(...),
    descricao: str = Form(...),
    link_projeto: Optional[str] = Form(None),
    tecnologias: str = Form(...),
    link_unico: Optional[str] = Form(None),
    link_backend: Optional[str] = Form(None),
    link_frontend: Optional[str] = Form(None),
    imagem: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    _=Depends(get_admin_atual)
):
    dados = ProjetoInput(
        nome=nome, resumo=resumo, descricao=descricao,
        link_projeto=link_projeto, tecnologias=tecnologias,
        link_unico=link_unico, link_backend=link_backend, link_frontend=link_frontend
    )
    return ProjetoService(db).criar(dados, imagem)

@router.get("", response_model=list[ProjetoOutput], responses={
    204: {"description": "Nenhum Registro Encontrado"},
})
def listar(db: Session = Depends(get_db)):
    return ProjetoService(db).listar()

@router.get("/{id}", response_model=ProjetoOutput, responses={
    204: {"description": "Nenhum Registro Encontrado"},
})
def buscar(id: int, db: Session = Depends(get_db)):
    return ProjetoService(db).buscar(id)

@router.put("/{id}", response_model=ProjetoOutput, responses={
    400: {"description": "Os campos não podem estar vazios"},
    401: {"description": "Credenciais inválidas"},
    409: {"description": "Projeto já registrado"},
})
def atualizar(
    id: int,
    nome: str = Form(...),
    resumo: str = Form(...),
    descricao: str = Form(...),
    link_projeto: Optional[str] = Form(None),
    tecnologias: str = Form(...),
    link_unico: Optional[str] = Form(None),
    link_backend: Optional[str] = Form(None),
    link_frontend: Optional[str] = Form(None),
    imagem: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    _=Depends(get_admin_atual)
):
    dados = ProjetoInput(
        nome=nome, resumo=resumo, descricao=descricao,
        link_projeto=link_projeto, tecnologias=tecnologias,
        link_unico=link_unico, link_backend=link_backend, link_frontend=link_frontend
    )
    return ProjetoService(db).atualizar(id, dados, imagem)

@router.delete("/{id}", status_code=204, responses={
    401: {"description": "Credenciais inválidas"},
})
def remover(id: int, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    ProjetoService(db).remover(id)