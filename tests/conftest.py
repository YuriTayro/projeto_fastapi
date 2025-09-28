# define fixtures que podem ser reutilizadas em
# diferentes módulos de teste em um projeto
# Uma fixture é como uma função que prepara dados
# ou estado necessários para o teste.

from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from projeto_fastapi.app import app
from projeto_fastapi.database import get_session
from projeto_fastapi.models import tabela_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client  # Fornece o cliente para o teste
    app.dependency_overrides.clear()


@pytest.fixture
def session():  # essa fixture session q será usada para
    # executar a função de teste no arquivo de test_db.py
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    tabela_registry.metadata.create_all(engine)

    with Session(engine) as session:  # O with garante que a
        # sessão será fechada corretamente no final, mesmo que ocorram erros.
        yield session  # entrega o resultado para a variavel session.

    tabela_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture  # fixture
def mock_db_time():
    return _mock_db_time
