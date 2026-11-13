"""Endpoints des ordres de fabrication.

JOUR 1 - APRÈS-MIDI : un exemple complet (POST /orders) est fourni ;
les autres endpoints sont à écrire par toi.
"""
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import case, func, select
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
@router.patch("/{order_id}/start", response_model=schemas.WorkOrderOut)
def start_order(order_id: int, db: Session = Depends(get_db)):
    """Démarre un ordre de fabrication (CREATED -> STARTED)."""
    order = db.get(models.WorkOrder, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Ordre introuvable")

    if order.status != "CREATED":
        raise HTTPException(
            status_code=409,
            detail=f"Impossible de démarrer un ordre au statut {order.status}",
        )

    order.status = "STARTED"
    db.commit()
    db.refresh(order)
    return order


# TODO : PATCH /orders/{order_id}/complete
#        -> refuser (409) si le statut n'est pas STARTED

@router.patch("/{order_id}/complete", response_model=schemas.WorkOrderOut)
def complete_order(order_id: int, db: Session = Depends(get_db)):
    """Termine un ordre de fabrication (STARTED -> COMPLETED)."""
    order = db.get(models.WorkOrder, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Ordre introuvable")

    if order.status != "STARTED":
        raise HTTPException(
            status_code=409,
            detail=f"Impossible de terminer un ordre au statut {order.status}",
        )

    order.status = "COMPLETED"
    db.commit()
    db.refresh(order)
    return order

# TODO : POST /orders/{order_id}/parts
#        -> refuser (409) si l'ordre n'est pas STARTED
#        -> refuser (409) si la quantité prévue est déjà atteinte


@router.post("/{order_id}/parts", response_model=schemas.PartOut, status_code=201)
def add_part(order_id: int, payload: schemas.PartCreate, db: Session = Depends(get_db)):
    """Enregistre une pièce produite pour un ordre démarré."""
    order = db.get(models.WorkOrder, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Ordre introuvable")

    # Règle 1 : on ne produit que sur un ordre démarré
    if order.status != "STARTED":
        raise HTTPException(status_code=409, detail="Impossible d'ajouter une pièce à un ordre non démarré")

    # Règle 2 : on ne dépasse pas la quantité prévue
    if len(order.parts) >= order.planned_quantity:
        raise HTTPException(status_code=409, detail="Quantité prévue déjà atteinte")

    part = models.Part(
        work_order_id=order_id,
        serial_number=payload.serial_number,
        quality_result=payload.quality_result,
    )
    db.add(part)
    db.commit()
    db.refresh(part)
    return part




# TODO : GET /orders/{order_id}/summary
#        -> pièces bonnes, rejetées, total, taux de rendement (%)
#        -> astuce : une seule requête SQL avec COUNT + CASE WHEN
@router.get("/{order_id}/summary", response_model=schemas.OrderSummary)
def get_order_summary(order_id: int, db: Session = Depends(get_db)):
    """Résumé de production : pièces bonnes, rejetées et taux de rendement."""
    order = db.get(models.WorkOrder, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Ordre introuvable")

    stmt = select(
        func.count(models.Part.id),
        func.count(case((models.Part.quality_result == "GOOD", 1))),
        func.count(case((models.Part.quality_result == "REJECTED", 1))),
    ).where(models.Part.work_order_id == order_id)

    total, good, rejected = db.execute(stmt).one()
    yield_percent = round(good * 100.0 / total, 2) if total > 0 else 0.0

    return schemas.OrderSummary(
        order_id=order_id,
        total_parts=total,
        good_parts=good,
        rejected_parts=rejected,
        yield_percent=yield_percent,
    )