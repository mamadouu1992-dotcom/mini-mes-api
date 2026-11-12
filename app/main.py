"""Point d'entrée de l'API.

Lancer : uvicorn app.main:app --reload
Documentation interactive : http://localhost:8000/docs
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (enregistre les tables auprès de Base)
from app.database import Base, engine
from app.routers import events, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crée les tables PostgreSQL au démarrage si elles n'existent pas
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Mini-MES API",
    description="API de traçabilité de production : ordres de fabrication, pièces et événements machine.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(orders.router)
app.include_router(events.router)


@app.get("/health", tags=["Système"])
def health():
    return {"status": "ok"}
