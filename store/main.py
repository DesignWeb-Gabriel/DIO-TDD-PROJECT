from fastapi import FastAPI

app = FastAPI(title="Store API", version="0.0.1")

# Importar e incluir as rotas após a criação do app
try:
    from store.routers import api_router

    app.include_router(api_router)
    print(f"✅ Rotas incluídas com sucesso. Total: {len(app.routes)} rotas")
except Exception as e:
    print(f"❌ Erro ao incluir rotas: {e}")
    raise e
