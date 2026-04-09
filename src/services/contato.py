import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from schemas.contato import ContatoInput
from core.config import settings

EMAIL_DESTINO  = "rafaporann@gmail.com"
EMAIL_REMETENTE = settings.EMAIL_REMETENTE
EMAIL_SENHA     = settings.EMAIL_SENHA


class ContatoService:

    def _validar_campos(self, dados: ContatoInput):
        campos_faltantes = []

        if not dados.nome or not dados.nome.strip():
            campos_faltantes.append("nome")

        if not dados.email or not dados.email.strip():
            campos_faltantes.append("email")

        if not dados.mensagem or len(dados.mensagem.strip()) < 3:
            campos_faltantes.append("mensagem")

        if campos_faltantes:
            raise HTTPException(
                status_code=400,
                detail={
                    "mensagem": "Campos obrigatórios não preenchidos",
                    "campos": campos_faltantes
                }
            )

    def enviar(self, dados: ContatoInput):
        self._validar_campos(dados)

        assunto = dados.assunto.strip() if dados.assunto and dados.assunto.strip() else "Sem assunto"

        # Monta o corpo do e-mail
        corpo = f"""
        <html>
            <body>
                <h2>Nova mensagem pelo portfólio</h2>
                <p><strong>Nome:</strong> {dados.nome}</p>
                <p><strong>E-mail:</strong> {dados.email}</p>
                <p><strong>Assunto:</strong> {assunto}</p>
                <hr>
                <p><strong>Mensagem:</strong></p>
                <p>{dados.mensagem}</p>
            </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Portfólio - {assunto}"
        msg["From"]    = EMAIL_REMETENTE
        msg["To"]      = EMAIL_DESTINO
        msg["Reply-To"] = dados.email  # ao responder, vai direto para quem enviou

        msg.attach(MIMEText(corpo, "html"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
                servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
                servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, msg.as_string())
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro ao enviar mensagem. Tente novamente mais tarde."
            )

        return {"mensagem": "Mensagem Enviada"}