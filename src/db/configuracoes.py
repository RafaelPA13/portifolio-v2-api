from sqlalchemy import Column, Integer, String, Date
from db.base import Base, BaseRepository

class Configuracao(Base):
    __tablename__ = "configuracoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    curriculo_nome = Column(String(255), nullable=True)
    curriculo_url = Column(String(500), nullable=True)
    dt_atualizacao = Column(Date, nullable=True)

class ConfiguracaoRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Configuracao)

    def buscar_unico(self):
        return self.db.query(Configuracao).first()