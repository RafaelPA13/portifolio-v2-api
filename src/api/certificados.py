from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.base import get_db
from schemas.certificados import CertificadoInput, CertificadoOutput
from services.certificados import CertificadoService
from core.security import get_admin_atual

router = APIRouter(prefix="/certificados", tags=["Certificados"])

@router.post("", status_code=201, responses={
    201: {"description": "Certificado Adicionado"},
    400: {"description": "Os campos não podem estar vazios"},
    401: {"description": "Credenciais inválidas"},
    409: {"description": "Certificado já registrado"},
})
def criar(dados: CertificadoInput, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    return CertificadoService(db).criar(dados)

@router.get("", response_model=list[CertificadoOutput], responses={
    204: {"description": "Nenhum Registro Encontrado"},
})
def listar(db: Session = Depends(get_db)):
    return CertificadoService(db).listar()

@router.get("/{id}", response_model=CertificadoOutput, responses={
    204: {"description": "Nenhum Registro Encontrado"},
    401: {"description": "Credenciais inválidas"},
})
def buscar(id: int, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    return CertificadoService(db).buscar(id)

@router.put("/{id}", response_model=CertificadoOutput, responses={
    400: {"description": "Os campos não podem estar vazios"},
    401: {"description": "Credenciais inválidas"},
    409: {"description": "Certificado já registrado"},
})
def atualizar(id: int, dados: CertificadoInput, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    return CertificadoService(db).atualizar(id, dados)

@router.delete("/{id}", status_code=204, responses={
    401: {"description": "Credenciais inválidas"},
})
def remover(id: int, db: Session = Depends(get_db), _=Depends(get_admin_atual)):
    CertificadoService(db).remover(id)