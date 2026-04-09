import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.admin import router as admin_router
from api.tecnologias import router as tecnologias_router
from api.projetos import router as projetos_router
from api.experiencias import router as experiencias_router
from api.certificados import router as certificados_router
from api.curriculo import router as curriculo_router

app = FastAPI(
    title="Portfólio API",
    description="API do portfólio pessoal",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar para o domínio do frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(admin_router)
app.include_router(tecnologias_router)
app.include_router(projetos_router)
app.include_router(experiencias_router)
app.include_router(certificados_router)
app.include_router(curriculo_router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Portfólio API rodando"}