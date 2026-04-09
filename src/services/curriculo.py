from datetime import date
from fastapi import HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.configuracoes import Configuracao, ConfiguracaoRepository
from core.storage import upload_pdf, deletar_pdf

class CurriculoService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = ConfiguracaoRepository(db)

    def upload(self, arquivo: UploadFile):
        # Borda: arquivo não enviado ou vazio
        if not arquivo or not arquivo.filename:
            raise HTTPException(status_code=400, detail="Selecione um arquivo PDF")

        # Borda: formato inadequado
        if arquivo.content_type != "application/pdf" or not arquivo.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Formato inadequado")

        nome_arquivo = arquivo.filename
        conteudo = arquivo.file.read()

        # Remove o PDF anterior do Supabase se existir
        config = self.repo.buscar_unico()
        if config and config.curriculo_url:
            deletar_pdf(config.curriculo_url)

        # Faz upload para o Supabase Storage
        url_publica = upload_pdf(conteudo, nome_arquivo)

        # Atualiza ou cria o registro no banco
        if config:
            config.curriculo_nome = nome_arquivo
            config.curriculo_url  = url_publica
            config.dt_atualizacao = date.today()
            self.repo.update(config)
        else:
            self.repo.insert(Configuracao(
                curriculo_nome=nome_arquivo,
                curriculo_url=url_publica,
                dt_atualizacao=date.today()
            ))

        return {"mensagem": "Currículo Atualizado"}

    def download(self):
        config = self.repo.buscar_unico()

        if not config or not config.curriculo_url:
            raise HTTPException(status_code=404, detail="Currículo não encontrado")

        # Redireciona para a URL pública do Supabase
        # O navegador/Postman vai baixar o arquivo diretamente de lá
        return RedirectResponse(
            url=config.curriculo_url,
            status_code=302
        )