import resend
from fastapi import HTTPException
from schemas.contato import ContatoInput
from core.config import settings

EMAIL_DESTINO = "rafaporann@gmail.com"

resend.api_key = settings.RESEND_API_KEY


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
                detail=f"Campos obrigatórios não preenchidos: {', '.join(campos_faltantes)}"
            )

    async def enviar(self, dados: ContatoInput):
        self._validar_campos(dados)

        assunto = dados.assunto.strip() if dados.assunto and dados.assunto.strip() else "Sem assunto"

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

        try:
            resend.Emails.send({
                "from": "Portfólio <onboarding@resend.dev>",
                "to": EMAIL_DESTINO,
                "reply_to": dados.email,
                "subject": f"Portfólio - {assunto}",
                "html": corpo,
            })
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao enviar mensagem: {str(e)}"
            )

        return {"mensagem": "Mensagem Enviada"}