"""Configuration partagée des tests (fixtures pytest).

Les tests qui utilisent db_client ou events_client ont besoin des bases
de données : PostgreSQL et MongoDB doivent tourner en local.
"""
import pytest
from fastapi.testclient import TestClient

from app.database import MONGO_DB, Base, engine, mongo_client
from app.main import app


@pytest.fixture
def client():
    """Client HTTP de test, sans base de données (pour /health)."""
    return TestClient(app)


@pytest.fixture
def db_client():
    """Client HTTP de test avec des tables PostgreSQL vides.

    Les tables sont recréées avant chaque test pour que les tests soient indépendants.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c


@pytest.fixture
def events_client(db_client):
    """Client HTTP de test avec une collection MongoDB machine_events vide (jour 2)."""
    mongo_client[MONGO_DB].machine_events.delete_many({})
    yield db_client
