from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.certificados import Certificado, CertificadoRepository
from db.tecnologias import TecnologiaRepository
from db.base import certificados_tecnologias
from schemas.certificados import CertificadoInput

class CertificadoService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = CertificadoRepository(db)
        self.repo_tecnologia = TecnologiaRepository(db)

    def _validar_campos(self, dados: CertificadoInput):
        campos_vazios = []
        if not dados.nome or not dados.nome.strip():
            campos_vazios.append("nome")
        if not dados.instituicao or not dados.instituicao.strip():
            campos_vazios.append("instituicao")
        if not dados.link or not dados.link.strip():
            campos_vazios.append("link")
        if not dados.dt_conclusao:
            campos_vazios.append("dt_conclusao")
        if campos_vazios:
            raise HTTPException(
                status_code=400,
                detail={"mensagem": "Os campos não podem estar vazios", "campos": campos_vazios}
            )

    def _verificar_duplicado(self, nome: str, ignorar_id: int = None):
        existente = self.db.query(Certificado).filter(
            Certificado.nome.ilike(nome.strip())
        ).first()
        if existente and existente.id != ignorar_id:
            raise HTTPException(status_code=409, detail="Certificado já registrado")

    def _resolver_tecnologias(self, tecnologias_str: str) -> list[int]:
        if not tecnologias_str or not tecnologias_str.strip():
            return []
        nomes = [t.strip() for t in tecnologias_str.split(",") if t.strip()]
        tecnologias = self.repo_tecnologia.buscar_por_nomes(nomes)
        return [t.id for t in tecnologias]

    def _inserir_tecnologias(self, certificado_id: int, tecnologia_ids: list[int]):
        for tecnologia_id in tecnologia_ids:
            self.db.execute(
                certificados_tecnologias.insert().values(
                    certificado_id=certificado_id,
                    tecnologia_id=tecnologia_id
                )
            )
        self.db.commit()

    def _atualizar_tecnologias(self, certificado_id: int, tecnologia_ids: list[int]):
        self.db.execute(
            certificados_tecnologias.delete().where(
                certificados_tecnologias.c.certificado_id == certificado_id
            )
        )
        self._inserir_tecnologias(certificado_id, tecnologia_ids)

    def criar(self, dados: CertificadoInput):
        self._validar_campos(dados)
        self._verificar_duplicado(dados.nome)

        novo = Certificado(
            nome=dados.nome.strip(),
            instituicao=dados.instituicao.strip(),
            carga_horaria=dados.carga_horaria,
            link=dados.link,
            dt_conclusao=dados.dt_conclusao,
            criado_em=date.today()
        )
        certificado = self.repo.insert(novo)

        tecnologia_ids = self._resolver_tecnologias(dados.tecnologias)
        if tecnologia_ids:
            self._inserir_tecnologias(certificado.id, tecnologia_ids)

        self.db.refresh(certificado)
        return certificado

    def listar(self):
        registros = self.db.query(Certificado).order_by(Certificado.criado_em.desc()).all()
        if not registros:
            raise HTTPException(status_code=400, detail="Nenhum Registro Encontrado")
        return registros

    def buscar(self, id: int):
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=400, detail="Nenhum Registro Encontrado")
        return registro

    def atualizar(self, id: int, dados: CertificadoInput):
        self._validar_campos(dados)
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=400, detail="Nenhum Registro Encontrado")

        self._verificar_duplicado(dados.nome, ignorar_id=id)

        registro.nome = dados.nome.strip()
        registro.instituicao = dados.instituicao.strip()
        registro.carga_horaria = dados.carga_horaria
        registro.link = dados.link
        registro.dt_conclusao = dados.dt_conclusao

        self.repo.update(registro)

        if dados.tecnologias is not None:
            tecnologia_ids = self._resolver_tecnologias(dados.tecnologias)
            self._atualizar_tecnologias(id, tecnologia_ids)

        self.db.refresh(registro)
        return registro

    def remover(self, id: int):
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=400, detail="Nenhum Registro Encontrado")
        self.repo.delete(id)