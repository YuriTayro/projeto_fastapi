# define fixtures que podem ser reutilizadas em
# diferentes módulos de teste em um projeto
# Uma fixture é como uma função que prepara dados
# ou estado necessários para o teste.

import pytest
from fastapi.testclient import TestClient

from projeto_fastapi.app import app, database


@pytest.fixture
def client():
    # Código de setup (antes do yield)
    yield TestClient(app)  # Fornece o cliente para o teste

    # Código de teardown (depois do yield)
    database.clear()  # Limpa o banco de dados após o teste
