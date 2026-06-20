from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.database import connect_to_mongo, close_mongo_connection
from app.routes import clientes, cep


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executado ao iniciar a aplicação
    await connect_to_mongo()
    yield
    # Executado ao desligar a aplicação
    await close_mongo_connection()


app = FastAPI(
    title="API de Cadastro e Gestão de Clientes",
    description=(
        "Trabalho final da disciplina CAC3024-09754 — Integração de Sistemas "
        "para Automação. Webservices REST com FastAPI + MongoDB, incluindo "
        "integração com o webservice externo ViaCEP."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Libera acesso de qualquer origem (útil para testar via navegador/Postman)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro das rotas
app.include_router(clientes.router)
app.include_router(cep.router)


@app.get("/api", tags=["Status"])
async def status_api():
    """Endpoint simples para verificar se a API está no ar."""
    return {
        "status": "online",
        "servico": "API de Cadastro e Gestão de Clientes",
        "documentacao": "/docs"
    }


# Serve a interface HTML (painel de testes) na raiz do site
app.mount("/", StaticFiles(directory="static", html=True), name="static")
