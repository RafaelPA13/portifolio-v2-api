from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from src.db.base import Base, BaseRepository, projetos_tecnologias, certificados_tecnologias, experiencias_tecnologias

class Tecnologia(Base):
    __tablename__ = "tecnologias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill = Column(String(150), nullable=False)
    dt_criacao = Column(Date, nullable=False)
    dt_atualizacao = Column(Date, nullable=True)
    
    projetos     = relationship("Projeto",     secondary=projetos_tecnologias,     back_populates="tecnologias")
    certificados = relationship("Certificado", secondary=certificados_tecnologias, back_populates="tecnologias")
    experiencias = relationship("Experiencia", secondary=experiencias_tecnologias, back_populates="experiencias")

class TecnologiaRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Tecnologia)