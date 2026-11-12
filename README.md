# Mini-MES API

![CI](https://github.com/mamadouu1992-dotcom/mini-mes-api/actions/workflows/ci.yml/badge.svg)

API REST de traçabilité de production inspirée d'un MES (Manufacturing Execution System) :
gestion des ordres de fabrication, des pièces produites et des événements machine.

## Contexte

<!-- À compléter (jour 2) : 3-4 phrases sur le problème métier. Ex. : dans une usine,
il faut savoir quelles pièces ont été produites pour quel ordre, avec quel résultat qualité,
et ce qui s'est passé sur les machines pendant la production. -->

## Architecture

```
            ┌──────────────┐
 Client ──► │  FastAPI     │ ──► PostgreSQL : ordres de fabrication, pièces (relationnel)
 (REST)     │  (Python 3)  │ ──► MongoDB    : événements machine (documents JSON flexibles)
            └──────────────┘
                   ▲
          pytest + GitHub Actions (CI)
```

## Technologies

- **Python 3.12**, **FastAPI**, **Pydantic**
- **PostgreSQL** avec **SQLAlchemy 2.0**
- **MongoDB** avec **PyMongo**
- **pytest** pour les tests
- **GitHub Actions** pour l'intégration continue

## Lancer le projet

Prérequis : PostgreSQL (utilisateur `mes`, mot de passe `mes`, base `mes`) et MongoDB
en local sur leurs ports par défaut (5432 et 27017). Pour utiliser d'autres valeurs, définis les variables d'environnement listées dans `.env.example`.

```bash
python -m venv .venv
.venv\Scripts\activate               # Windows (macOS/Linux : source .venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentation interactive : http://localhost:8000/docs

## Lancer les tests

```bash
pytest -v
```

## Endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/health` | État de l'API |
| POST | `/orders` | Créer un ordre de fabrication |
| GET | `/orders/{id}` | Consulter un ordre |
| PATCH | `/orders/{id}/start` | Démarrer un ordre |
| PATCH | `/orders/{id}/complete` | Compléter un ordre |
| POST | `/orders/{id}/parts` | Enregistrer une pièce produite |
| GET | `/orders/{id}/summary` | Résumé : bonnes, rejetées, rendement |
| POST | `/events` | Enregistrer un événement machine |
| GET | `/events` | Lister les événements (filtres : machine, type) |

## Choix techniques

<!-- À compléter (jour 2) : pourquoi PostgreSQL pour les ordres, pourquoi MongoDB pour les événements,
quelles règles métier sont testées. -->
