from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.base import get_db
from src.schemas.admin import LoginInput, TokenOutput
from src.services.admin import AdminService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/login",
    response_model=TokenOutput,
    responses={
        200: {"description": "Login realizado com sucesso"},
        400: {"description": "Campos obrigatórios não preenchidos"},
        401: {"description": "Credenciais inválidas"},
    }
)
def login(dados: LoginInput, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.login(dados)