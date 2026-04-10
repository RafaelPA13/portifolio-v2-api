from datetime import date
from fastapi import HTTPException
from db.tecnologias import Tecnologia, TecnologiaRepository
from schemas.tecnologias import TecnologiaInput

class TecnologiaService:

    def __init__(self, db):
        self.repo = TecnologiaRepository(db)

    # Validação de campos vazios 
    def _validar_campos(self, dados: TecnologiaInput):
        campos_vazios = []
        if not dados.skill or not dados.skill.strip():
            campos_vazios.append("skill")
        if campos_vazios:
            raise HTTPException(
                status_code=400,
                detail={"mensagem": "Os campos não podem estar vazios", "campos": campos_vazios}
            )

    # Verificar duplicidade 
    def _verificar_duplicado(self, skill: str, ignorar_id: int = None):
        existente = self.repo.buscar_por_skill(skill.strip())
        if existente and existente.id != ignorar_id:
            raise HTTPException(status_code=409, detail="Tecnologia já registrada")

    # POST 
    def criar(self, dados: TecnologiaInput):
        self._validar_campos(dados)
        self._verificar_duplicado(dados.skill)

        nova = Tecnologia(
            skill=dados.skill.strip(),
            dt_criacao=date.today(),
            dt_atualizacao=date.today()
        )
        return self.repo.insert(nova)

    # GET ALL 
    def listar(self):
        registros = self.repo.select_all()
        if not registros:
            raise HTTPException(status_code=204, detail="Nenhum Registro Encontrado")
        return registros

    # GET BY ID 
    def buscar(self, id: int):
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=204, detail="Nenhum Registro Encontrado")
        return registro

    # PUT 
    def atualizar(self, id: int, dados: TecnologiaInput):
        self._validar_campos(dados)
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=204, detail="Nenhum Registro Encontrado")

        self._verificar_duplicado(dados.skill, ignorar_id=id)

        registro.skill = dados.skill.strip()
        registro.dt_atualizacao = date.today()
        return self.repo.update(registro)

    # DELETE 
    def remover(self, id: int):
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=204, detail="Nenhum Registro Encontrado")
        self.repo.delete(id)