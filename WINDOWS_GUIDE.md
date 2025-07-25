# Guia para Windows - TDD Project

Este projeto foi originalmente configurado para sistemas Unix/Linux com `make`, mas aqui estão as instruções para executar no Windows.

## Pré-requisitos

- Python 3.12+ instalado
- Poetry instalado (`pip install poetry`)

## Como executar o projeto

### Método 1: Usando os arquivos .bat (Mais fácil)

Criamos scripts batch para facilitar a execução:

- **`run.bat`** - Executa o servidor principal (store.main)
- **`run_src.bat`** - Executa o servidor alternativo (src.main)
- **`test.bat`** - Executa os testes

Apenas dê duplo clique no arquivo desejado ou execute no PowerShell:

```powershell
.\run.bat
```

### Método 2: Comandos diretos no terminal

```powershell
# Instalar dependências
poetry install

# Executar servidor principal
poetry run uvicorn store.main:app --reload

# Executar servidor alternativo (com endpoints básicos)
poetry run uvicorn src.main:app --reload

# Executar testes
poetry run pytest
```

### Método 3: Instalar Make para Windows (Opcional)

Se preferir usar o Makefile original:

1. Instale o Chocolatey: https://chocolatey.org/install
2. Execute: `choco install make`
3. Agora pode usar: `make run`

## Endpoints disponíveis

### Store App (localhost:8000)

- `/docs` - Documentação Swagger
- `/redoc` - Documentação ReDoc

### Src App (localhost:8000)

- `/` - Endpoint raiz ("Hello World")
- `/health` - Health check
- `/docs` - Documentação Swagger

## Testando a aplicação

Abra o navegador em:

- http://localhost:8000/docs (Documentação interativa)
- http://localhost:8000/redoc (Documentação alternativa)

Para a aplicação src:

- http://localhost:8000/ (Hello World)
- http://localhost:8000/health (Health check)
