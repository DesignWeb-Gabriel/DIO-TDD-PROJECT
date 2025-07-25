@echo off
echo Iniciando servidor FastAPI...
poetry run uvicorn store.main:app --reload
pause
