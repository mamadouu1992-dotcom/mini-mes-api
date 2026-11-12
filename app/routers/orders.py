"""Endpoints des ordres de fabrication.

JOUR 1 - APRÈS-MIDI : un exemple complet (POST /orders) est fourni ;
les autres endpoints sont à écrire par toi.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/orders", tags=["Ordres de fabrication"])


@router.post("", response_model=schemas.WorkOrderOut, status_code=201)
def create_order(payload: schemas.WorkOrderCreate, db: Session = Depends(get_db)):
    """Exemple complet : crée un ordre de fabrication."""
    order = models.WorkOrder(product=payload.product, planned_quantity=payload.planned_quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/{order_id}", response_model=schemas.WorkOrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(models.WorkOrder, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Ordre introuvable")
    return order


# TODO : PATCH /orders/{order_id}/start
#        -> refuser (409) si le statut n'est pas CREATED

# TODO : PATCH /orders/{order_id}/complete
#        -> refuser (409) si le statut n'est pas STARTED

# TODO : POST /orders/{order_id}/parts
#        -> refuser (409) si l'ordre n'est pas STARTED
#        -> refuser (409) si la quantité prévue est déjà atteinte

# TODO : GET /orders/{order_id}/summary
#        -> pièces bonnes, rejetées, total, taux de rendement (%)
#        -> astuce : une seule requête SQL avec COUNT + CASE WHEN
