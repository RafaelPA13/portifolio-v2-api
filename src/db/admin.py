from sqlalchemy import Column, Integer, String, Date
from src.db.base import Base, BaseRepository

class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(150), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    dt_criacao = Column(Date, nullable=False)

class AdminRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Admin)

    def buscar_por_email(self, email: str):
        return self.db.query(Admin).filter(Admin.email == email).first()