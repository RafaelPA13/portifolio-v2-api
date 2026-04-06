from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.core.config import settings

# Engine e Sessão
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Base declarativa
class Base(DeclarativeBase):
    pass

# Tabelas de associação N:N 
projetos_tecnologias = Table(
    "projetos_tecnologias",
    Base.metadata,
    Column("projeto_id",    Integer, ForeignKey("projetos.id"),    primary_key=True),
    Column("tecnologia_id", Integer, ForeignKey("tecnologias.id"), primary_key=True)
)

certificados_tecnologias = Table(
    "certificados_tecnologias",
    Base.metadata,
    Column("certificado_id", Integer, ForeignKey("certificados.id"), primary_key=True),
    Column("tecnologia_id",  Integer, ForeignKey("tecnologias.id"),  primary_key=True)
)

experiencias_tecnologias = Table(
    "experiencias_tecnologias",
    Base.metadata,
    Column("experiencia_id", Integer, ForeignKey("experiencias.id"), primary_key=True),
    Column("tecnologia_id",  Integer, ForeignKey("tecnologias.id"),  primary_key=True)
)

# Dependency Injection (usado nos endpoints) 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Classe base de repositório 
class BaseRepository:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def select_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def select_all(self):
        return self.db.query(self.model).all()

    def insert(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj):
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        obj = self.select_by_id(id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True