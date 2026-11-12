"""Événements machine stockés dans MongoDB (NoSQL).

JOUR 2 - MATIN : à écrire par toi.

Exemple de document :
{
    "machine": "PRESS-01",
    "type": "ALARM",            # ALARM, STOP, START, ...
    "code": "E42",
    "details": {"pression": 182.5, "operateur": "J. Tremblay"},
    "timestamp": "2026-11-12T09:30:00"
}
Le champ "details" varie d'une machine à l'autre : c'est pour ça qu'on utilise MongoDB.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["Événements machine"])

# TODO : POST /events
#        -> db = get_mongo(); db.machine_events.insert_one(...)
#        -> attention : renvoyer l'_id converti en str

# TODO : GET /events?machine=PRESS-01&type=ALARM
#        -> filtres optionnels, tri par timestamp décroissant
