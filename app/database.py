"""Connexions aux bases de données : PostgreSQL (relationnel) et MongoDB (NoSQL)."""
import os

from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# --- PostgreSQL -------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://mes:mes@localhost:5432/mes")

engine = create_engine(DATABASE_URL)  # ne se connecte qu'au premier usage
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Classe de base pour tous les modèles SQLAlchemy (voir models.py)."""


def get_db():
    """Dépendance FastAPI : ouvre une session SQL par requête, puis la ferme."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- MongoDB ----------------------------------------------------------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "mes")

mongo_client = MongoClient(MONGO_URL)  # ne se connecte qu'au premier usage


def get_mongo():
    """Dépendance FastAPI : renvoie la base MongoDB du projet."""
    return mongo_client[MONGO_DB]
