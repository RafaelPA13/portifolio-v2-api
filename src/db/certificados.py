from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from db.base import Base, BaseRepository, certificados_tecnologias

class Certificado(Base):
    __tablename__ = "certificados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    instituicao = Column(String(150), nullable=False)
    carga_horaria = Column(Integer, nullable=True)
    link = Column(String(150), nullable=True)
    dt_conclusao = Column(Date, nullable=True)
    criado_em = Column(Date, nullable=False)
    
    tecnologias = relationship("Tecnologia", secondary=certificados_tecnologias, back_populates="certificados")

class CertificadoRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Certificado)