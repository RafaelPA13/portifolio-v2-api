import os
import shutil
from datetime import date
from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db.configuracoes import Configuracao, ConfiguracaoRepository

# Pasta base do projeto (onde está o main.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # sobe de services/ para src/

CURRICULO_DIR = os.path.join(BASE_DIR, "static", "curriculo")
CURRICULO_DIR_RELATIVO = os.path.join("static", "curriculo")


class CurriculoService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = ConfiguracaoRepository(db)

    def upload(self, arquivo: UploadFile):
        if not arquivo or not arquivo.filename:
            raise HTTPException(status_code=400, detail="Selecione um arquivo PDF")

        if arquivo.content_type != "application/pdf" or not arquivo.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Formato inadequado")

        os.makedirs(CURRICULO_DIR, exist_ok=True)

        # Usa o nome original do arquivo enviado
        nome_arquivo = arquivo.filename
        caminho_absoluto = os.path.join(CURRICULO_DIR, nome_arquivo)
        caminho_relativo = os.path.join(CURRICULO_DIR_RELATIVO, nome_arquivo)

        # Remove o arquivo anterior se existir e for diferente
        config = self.repo.buscar_unico()
        if config and config.curriculo_url:
            caminho_antigo = os.path.join(BASE_DIR, config.curriculo_url)
            if os.path.exists(caminho_antigo) and caminho_antigo != caminho_absoluto:
                os.remove(caminho_antigo)

        with open(caminho_absoluto, "wb") as destino:
            shutil.copyfileobj(arquivo.file, destino)

        # Salva caminho relativo no banco
        if config:
            config.curriculo_nome = nome_arquivo
            config.curriculo_url  = caminho_relativo
            config.dt_atualizacao = date.today()
            self.repo.update(config)
        else:
            self.repo.insert(Configuracao(
                curriculo_nome=nome_arquivo,
                curriculo_url=caminho_relativo,
                dt_atualizacao=date.today()
            ))

        return {"mensagem": "Currículo Atualizado"}

    def download(self):
        config = self.repo.buscar_unico()

        if not config or not config.curriculo_url:
            raise HTTPException(status_code=404, detail="Currículo não encontrado")

        # Reconstrói o caminho absoluto para servir o arquivo
        caminho_absoluto = os.path.join(BASE_DIR, config.curriculo_url)

        if not os.path.exists(caminho_absoluto):
            raise HTTPException(status_code=404, detail="Currículo não encontrado")

        return FileResponse(
            path=caminho_absoluto,
            media_type="application/pdf",
            filename=config.curriculo_nome,
            headers={"Content-Disposition": f"attachment; filename={config.curriculo_nome}"}
        )