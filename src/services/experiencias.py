from fastapi import HTTPException
from sqlalchemy import nulls_first
from sqlalchemy.orm import Session
from db.experiencias import Experiencia, ExperienciaRepository
from db.tecnologias import TecnologiaRepository
from db.base import experiencias_tecnologias
from schemas.experiencias import ExperienciaInput

class ExperienciaService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = ExperienciaRepository(db)
        self.repo_tecnologia = TecnologiaRepository(db)

    def _validar_campos(self, dados: ExperienciaInput):
        campos_vazios = []
        if not dados.cargo or not dados.cargo.strip():
            campos_vazios.append("cargo")
        if not dados.empresa or not dados.empresa.strip():
            campos_vazios.append("empresa")
        if not dados.descricao or not dados.descricao.strip():
            campos_vazios.append("descricao")
        if not dados.dt_inicio:
            campos_vazios.append("dt_inicio")
        if campos_vazios:
            raise HTTPException(
                status_code=400,
                detail={"mensagem": "Os campos não podem estar vazios", "campos": campos_vazios}
            )

    def _verificar_duplicado(self, cargo: str, empresa: str, ignorar_id: int = None):
        existente = self.db.query(Experiencia).filter(
            Experiencia.cargo.ilike(cargo.strip()),
            Experiencia.empresa.ilike(empresa.strip())
        ).first()
        if existente and existente.id != ignorar_id:
            raise HTTPException(status_code=409, detail="Experiência já registrada")

    def _resolver_tecnologias(self, tecnologias_str: str) -> list[int]:
        if not tecnologias_str or not tecnologias_str.strip():
            return []
        nomes = [t.strip() for t in tecnologias_str.split(",") if t.strip()]
        tecnologias = self.repo_tecnologia.buscar_por_nomes(nomes)
        return [t.id for t in tecnologias]

    def _inserir_tecnologias(self, experiencia_id: int, tecnologia_ids: list[int]):
        for tecnologia_id in tecnologia_ids:
            self.db.execute(
                experiencias_tecnologias.insert().values(
                    experiencia_id=experiencia_id,
                    tecnologia_id=tecnologia_id
                )
            )
        self.db.commit()

    def _atualizar_tecnologias(self, experiencia_id: int, tecnologia_ids: list[int]):
        self.db.execute(
            experiencias_tecnologias.delete().where(
                experiencias_tecnologias.c.experiencia_id == experiencia_id
            )
        )
        self._inserir_tecnologias(experiencia_id, tecnologia_ids)

    def criar(self, dados: ExperienciaInput):
        self._validar_campos(dados)
        self._verificar_duplicado(dados.cargo, dados.empresa)

        nova = Experiencia(
            cargo=dados.cargo.strip(),
            empresa=dados.empresa.strip(),
            descricao=dados.descricao,
            dt_inicio=dados.dt_inicio,
            dt_fim=dados.dt_fim,
            atual=dados.atual
        )
        experiencia = self.repo.insert(nova)

        tecnologia_ids = self._resolver_tecnologias(dados.tecnologias)
        if tecnologia_ids:
            self._inserir_tecnologias(experiencia.id, tecnologia_ids)

        self.db.refresh(experiencia)
        return experiencia

    def listar(self):
        registros = self.db.query(Experiencia).order_by(
            nulls_first(Experiencia.dt_fim.desc())
        ).all()
        if not registros:
            raise HTTPException(status_code=204, detail="Nenhum Registro Encontrado")
        return registros

    def buscar(self, id: int):
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=204, detail="Nenhum Registro Encontrado")
        return registro

    def atualizar(self, id: int, dados: ExperienciaInput):
        self._validar_campos(dados)
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=204, detail="Nenhum Registro Encontrado")

        self._verificar_duplicado(dados.cargo, dados.empresa, ignorar_id=id)

        registro.cargo = dados.cargo.strip()
        registro.empresa = dados.empresa.strip()
        registro.descricao = dados.descricao
        registro.dt_inicio = dados.dt_inicio
        registro.dt_fim = dados.dt_fim
        registro.atual = dados.atual

        self.repo.update(registro)

        if dados.tecnologias is not None:
            tecnologia_ids = self._resolver_tecnologias(dados.tecnologias)
            self._atualizar_tecnologias(id, tecnologia_ids)

        self.db.refresh(registro)
        return registro

    def remover(self, id: int):
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=204, detail="Nenhum Registro Encontrado")
        self.repo.delete(id)