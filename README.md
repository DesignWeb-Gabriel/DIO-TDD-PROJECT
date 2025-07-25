# TDD Project

Projeto de exemplo demonstrando Test-Driven Development (TDD) com Python, FastAPI, e pytest.

## 🚀 Configuração do Ambiente

### Pré-requisitos
- Python 3.12+
- Poetry para gerenciamento de dependências

### Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
poetry install
```

## 🧪 Executando os Testes

### Todos os testes
```bash
poetry run pytest -v
```

### Testes específicos
```bash
# Apenas testes da calculadora
poetry run pytest tests/test_calculator.py -v

# Com coverage
poetry run pytest --cov=src tests/
```

### Testes por marcadores
```bash
# Apenas testes unitários
poetry run pytest -m unit

# Testes de integração
poetry run pytest -m integration
```

## 🏃‍♂️ Executando a Aplicação

### Servidor de desenvolvimento
```bash
poetry run python run_server.py
```

### Usando uvicorn diretamente
```bash
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: http://localhost:8000

### Documentação da API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 Estrutura do Projeto

```
DIO TDD PROJECT/
├── src/                    # Código fonte
│   ├── __init__.py
│   ├── main.py            # Aplicação FastAPI
│   └── calculator.py      # Módulo calculadora
├── tests/                 # Testes
│   ├── __init__.py
│   ├── test_calculator.py # Testes da calculadora
│   └── test_fastapi_example.py # Testes da API
├── docs/                  # Documentação
├── pyproject.toml         # Configuração do Poetry
├── pytest.ini            # Configuração do pytest
├── run_server.py          # Script para executar servidor
└── README.md             # Este arquivo
```

## 🔄 Metodologia TDD

Este projeto segue o ciclo TDD:

1. **RED** 🔴: Escrever um teste que falha
2. **GREEN** 🟢: Escrever o código mínimo para passar no teste
3. **REFACTOR** 🔵: Melhorar o código mantendo os testes passando

### Exemplo de Ciclo TDD

1. Escreva um teste que falha:
```python
def test_add_two_numbers(self):
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5
```

2. Execute o teste (deve falhar):
```bash
poetry run pytest tests/test_calculator.py::TestCalculator::test_add_two_numbers -v
```

3. Implemente o código mínimo:
```python
class Calculator:
    def add(self, a, b):
        return a + b
```

4. Execute o teste novamente (deve passar):
```bash
poetry run pytest tests/test_calculator.py::TestCalculator::test_add_two_numbers -v
```

5. Refatore se necessário

## 🛠️ Ferramentas Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **pytest**: Framework de testes
- **pytest-asyncio**: Suporte a testes assíncronos
- **httpx**: Cliente HTTP para testes
- **uvicorn**: Servidor ASGI
- **pydantic**: Validação de dados
- **motor**: Driver MongoDB assíncrono
- **pre-commit**: Hooks de pré-commit

## ✅ Boas Práticas

- Escreva testes antes do código (TDD)
- Use nomes descritivos para testes
- Mantenha testes simples e focados
- Organize testes em classes temáticas
- Use fixtures para setup comum
- Execute testes frequentemente

## 📊 Comandos Úteis

```bash
# Instalar dependências
poetry install

# Adicionar nova dependência
poetry add package_name

# Adicionar dependência de desenvolvimento
poetry add --group dev package_name

# Atualizar dependências
poetry update

# Ver dependências instaladas
poetry show

# Ativar shell do poetry
poetry shell
```
