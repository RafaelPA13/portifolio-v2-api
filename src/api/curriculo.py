from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from db.base import get_db
from core.security import get_admin_atual
from services.curriculo import CurriculoService

router = APIRouter(prefix="/curriculo", tags=["Currículo"])

@router.post("/upload", dependencies=[Depends(get_admin_atual)])
def upload(
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return CurriculoService(db).upload(arquivo)

@router.get("/download")
def download(db: Session = Depends(get_db)):
    return CurriculoService(db).download()