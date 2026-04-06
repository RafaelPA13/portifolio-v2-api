from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.db.base import Base, BaseRepository, projetos_tecnologias
import enum

class TipoRepositorio(str, enum.Enum):
    frontend = "frontend"
    backend = "backend"
    unico = "único"

class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    resumo = Column(String(300), nullable=False)
    descricao = Column(Text, nullable=False)
    imagem = Column(String(2000), nullable=True)
    link_projeto = Column(String(2000), nullable=True)
    criado_em = Column(Date, nullable=False)

    repositorios = relationship("ProjetoRepositorio", back_populates="projeto", cascade="all, delete-orphan")
    tecnologias  = relationship("Tecnologia", secondary=projetos_tecnologias, back_populates="projetos")

class ProjetoRepositorio(Base):
    __tablename__ = "projetos_repositorios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=False)
    link = Column(String(2000), nullable=False)
    tipo = Column(Enum(TipoRepositorio), nullable=False)

    projeto = relationship("Projeto", back_populates="repositorios")

class ProjetoRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Projeto)

class ProjetoRepositorioRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, ProjetoRepositorio)