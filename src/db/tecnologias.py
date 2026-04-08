from sqlalchemy import Column, Integer, String, Date, func
from sqlalchemy.orm import relationship
from db.base import Base, BaseRepository, projetos_tecnologias, certificados_tecnologias, experiencias_tecnologias

class Tecnologia(Base):
    __tablename__ = "tecnologias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill = Column(String(150), nullable=False)
    dt_criacao = Column(Date, nullable=False)
    dt_atualizacao = Column(Date, nullable=True)
    
    projetos     = relationship("Projeto",     secondary=projetos_tecnologias,     back_populates="tecnologias")
    certificados = relationship("Certificado", secondary=certificados_tecnologias, back_populates="tecnologias")
    experiencias = relationship("Experiencia", secondary=experiencias_tecnologias, back_populates="tecnologias")

class TecnologiaRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Tecnologia)
        
    def buscar_por_skill(self, skill: str):
        return self.db.query(Tecnologia).filter(
            Tecnologia.skill.ilike(skill)
        ).first()

    def buscar_por_ids(self, ids: list[int]):
        return self.db.query(Tecnologia).filter(Tecnologia.id.in_(ids)).all()

    def buscar_por_nomes(self, nomes: list[str]):
        nomes_lower = [n.strip().lower() for n in nomes]
        return self.db.query(Tecnologia).filter(
            func.lower(Tecnologia.skill).in_(nomes_lower)
        ).all()