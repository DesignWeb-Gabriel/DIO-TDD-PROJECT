"""Aplicação FastAPI principal."""

from fastapi import FastAPI

app = FastAPI(
    title="TDD Project API", description="Exemplo de API usando TDD", version="0.0.1"
)


@app.get("/")
async def read_root():
    """Endpoint raiz da API."""
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    """Endpoint para verificação da saúde da API."""
    return {"status": "healthy"}
