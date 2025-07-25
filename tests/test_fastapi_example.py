"""Exemplo de testes para API FastAPI."""

import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """Cliente de teste para a API."""
    return TestClient(app)


def test_read_root(client):
    """Teste para o endpoint raiz."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_health_check(client):
    """Teste para o endpoint de health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
