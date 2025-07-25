@echo off
echo Iniciando servidor FastAPI (src)...
poetry run uvicorn src.main:app --reload
pause
