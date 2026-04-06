from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.admin import router as admin_router

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

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Portfólio API rodando"}