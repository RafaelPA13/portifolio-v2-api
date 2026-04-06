from sqlalchemy import Column, Integer, String, Text, Date, Boolean
from sqlalchemy.orm import relationship
from src.db.base import Base, BaseRepository, experiencias_tecnologias

class Experiencia(Base):
    __tablename__ = "experiencias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cargo = Column(String(150), nullable=False)
    empresa = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    dt_inicio = Column(Date, nullable=False)
    dt_fim = Column(Date, nullable=True)
    atual = Column(Boolean, default=False, nullable=False)
    
    tecnologias = relationship("Tecnologia", secondary=experiencias_tecnologias, back_populates="experiencias")

class ExperienciaRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Experiencia)