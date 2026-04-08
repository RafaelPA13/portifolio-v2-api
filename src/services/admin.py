from fastapi import HTTPException
from db.admin import AdminRepository
from core.security import verificar_senha, criar_token
from schemas.admin import LoginInput, TokenOutput


class AdminService:

    def __init__(self, db):
        self.repo = AdminRepository(db)

    def login(self, dados: LoginInput) -> TokenOutput:

        # Borda: campos vazios
        if not dados.email or not dados.email.strip():
            raise HTTPException(status_code=400, detail="email_obrigatorio")

        if not dados.senha or not dados.senha.strip():
            raise HTTPException(status_code=400, detail="senha_obrigatoria")

        # Busca admin pelo email
        admin = self.repo.buscar_por_email(dados.email.strip())

        # Borda: email inexistente ou senha errada
        # Mesmo comportamento para não revelar se o email existe
        if not admin or not verificar_senha(dados.senha, admin.senha_hash):
            raise HTTPException(status_code=401, detail="credenciais_invalidas")

        # Gera e retorna o token
        token = criar_token({"sub": str(admin.id), "email": admin.email})
        return TokenOutput(access_token=token)