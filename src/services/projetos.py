from datetime import date
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from db.projetos import Projeto, ProjetoRepositorio, TipoRepositorio, ProjetoRepository, ProjetoRepositorioRepository
from db.tecnologias import TecnologiaRepository
from db.base import projetos_tecnologias
from schemas.projetos import ProjetoInput
from core.storage import upload_imagem, deletar_imagem

class ProjetoService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = ProjetoRepository(db)
        self.repo_repositorio = ProjetoRepositorioRepository(db)
        self.repo_tecnologia = TecnologiaRepository(db)

    # Validação de campos 
    def _validar_campos(self, dados: ProjetoInput):
        campos_vazios = []
        if not dados.nome or not dados.nome.strip():
            campos_vazios.append("nome")
        if not dados.resumo or not dados.resumo.strip():
            campos_vazios.append("resumo")
        if not dados.descricao or not dados.descricao.strip():
            campos_vazios.append("descricao")
        if campos_vazios:
            raise HTTPException(
                status_code=400,
                detail={"mensagem": "Os campos não podem estar vazios", "campos": campos_vazios}
            )

    # Verificar duplicidade
    def _verificar_duplicado(self, nome: str, ignorar_id: int = None):
        existente = self.db.query(Projeto).filter(
            Projeto.nome.ilike(nome.strip())
        ).first()
        if existente and existente.id != ignorar_id:
            raise HTTPException(status_code=409, detail="Projeto já registrado")

    # Buscar ids das tecnologias pelo nome
    def _resolver_tecnologias(self, tecnologias_str: str) -> list[int]:
        if not tecnologias_str or not tecnologias_str.strip():
            return []
        nomes = [t.strip() for t in tecnologias_str.split(",") if t.strip()]
        tecnologias = self.repo_tecnologia.buscar_por_nomes(nomes)
        return [t.id for t in tecnologias]

    # Inserir projetos_tecnologias
    def _inserir_tecnologias(self, projeto_id: int, tecnologia_ids: list[int]):
        for tecnologia_id in tecnologia_ids:
            self.db.execute(
                projetos_tecnologias.insert().values(
                    projeto_id=projeto_id,
                    tecnologia_id=tecnologia_id
                )
            )
        self.db.commit()

    # Atualizar projetos_tecnologias
    def _atualizar_tecnologias(self, projeto_id: int, tecnologia_ids: list[int]):
        # Remove todas as associações atuais e recria
        self.db.execute(
            projetos_tecnologias.delete().where(
                projetos_tecnologias.c.projeto_id == projeto_id
            )
        )
        self._inserir_tecnologias(projeto_id, tecnologia_ids)

    # Inserir projetos_repositorios
    def _inserir_repositorios(self, projeto_id: int, dados: ProjetoInput):
        print("TipoRepositorio.unico =", TipoRepositorio.unico, repr(TipoRepositorio.unico.value))
        if dados.link_unico and dados.link_unico.strip():
            self.db.add(ProjetoRepositorio(
                projeto_id=projeto_id,
                link=dados.link_unico.strip(),
                tipo=TipoRepositorio.unico.value
            ))
        else:
            if dados.link_backend and dados.link_backend.strip():
                self.db.add(ProjetoRepositorio(
                    projeto_id=projeto_id,
                    link=dados.link_backend.strip(),
                    tipo=TipoRepositorio.backend.value
                ))
            if dados.link_frontend and dados.link_frontend.strip():
                self.db.add(ProjetoRepositorio(
                    projeto_id=projeto_id,
                    link=dados.link_frontend.strip(),
                    tipo=TipoRepositorio.frontend.value
                ))
        self.db.commit()

    # Atualizar projetos_repositorios
    def _atualizar_repositorios(self, projeto_id: int, dados: ProjetoInput):
        # Remove todos os repositórios atuais e recria
        self.db.query(ProjetoRepositorio).filter(
            ProjetoRepositorio.projeto_id == projeto_id
        ).delete()
        self.db.commit()
        self._inserir_repositorios(projeto_id, dados)

    # POST
    def criar(self, dados: ProjetoInput, imagem: UploadFile = None):
        self._validar_campos(dados)
        self._verificar_duplicado(dados.nome)

        imagem_url = None
        if imagem:
            conteudo = imagem.file.read()
            imagem_url = upload_imagem(conteudo, imagem.content_type, pasta="projetos")

        novo = Projeto(
            nome=dados.nome.strip(),
            resumo=dados.resumo.strip(),
            descricao=dados.descricao.strip(),
            imagem=imagem_url,
            link_projeto=dados.link_projeto,
            criado_em=date.today()
        )
        projeto = self.repo.insert(novo)

        tecnologia_ids = self._resolver_tecnologias(dados.tecnologias)
        if tecnologia_ids:
            self._inserir_tecnologias(projeto.id, tecnologia_ids)

        self._inserir_repositorios(projeto.id, dados)

        self.db.refresh(projeto)
        return projeto

    # GET ALL
    def listar(self):
        registros = self.db.query(Projeto).order_by(Projeto.criado_em.desc()).all()
        if not registros:
            raise HTTPException(status_code=400, detail="Nenhum Registro Encontrado")
        return registros

    # GET BY ID
    def buscar(self, id: int):
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=400, detail="Nenhum Registro Encontrado")
        return registro

    # PUT
    def atualizar(self, id: int, dados: ProjetoInput, imagem: UploadFile = None):
        self._validar_campos(dados)
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=400, detail="Nenhum Registro Encontrado")

        self._verificar_duplicado(dados.nome, ignorar_id=id)

        if imagem:
            if registro.imagem:
                deletar_imagem(registro.imagem)
            conteudo = imagem.file.read()
            registro.imagem = upload_imagem(conteudo, imagem.content_type, pasta="projetos")

        registro.nome = dados.nome.strip()
        registro.resumo = dados.resumo.strip()
        registro.descricao = dados.descricao.strip()
        registro.link_projeto = dados.link_projeto

        self.repo.update(registro)

        if dados.tecnologias is not None:
            tecnologia_ids = self._resolver_tecnologias(dados.tecnologias)
            self._atualizar_tecnologias(id, tecnologia_ids)

        if any([dados.link_unico, dados.link_backend, dados.link_frontend]):
            self._atualizar_repositorios(id, dados)

        self.db.refresh(registro)
        return registro

    # DELETE
    def remover(self, id: int):
        registro = self.repo.select_by_id(id)
        if not registro:
            raise HTTPException(status_code=400, detail="Nenhum Registro Encontrado")
        if registro.imagem:
            deletar_imagem(registro.imagem)
        self.repo.delete(id)  # cascade cuida das tabelas relacionadas