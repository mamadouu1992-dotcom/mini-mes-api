"""Tables PostgreSQL (SQLAlchemy 2.0).

JOUR 1 - APRÈS-MIDI : c'est à toi de compléter ce fichier.
"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class WorkOrder(Base):
    """Un ordre de fabrication."""

    __tablename__ = "work_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped[str] = mapped_column(String(100))
    planned_quantity: Mapped[int] = mapped_column(Integer)
    # Statuts possibles : CREATED -> STARTED -> COMPLETED
    status: Mapped[str] = mapped_column(String(20), default="CREATED")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    parts: Mapped[list["Part"]] = relationship(back_populates="work_order")


class Part(Base):
    """Une pièce produite dans un ordre de fabrication."""

    __tablename__ = "parts"

    id: Mapped[int] = mapped_column(primary_key=True)
    work_order_id: Mapped[int] = mapped_column(ForeignKey("work_orders.id"))

    # TODO : ajoute les colonnes
    #   - serial_number (texte, unique)
    #   - quality_result ("GOOD" ou "REJECTED")
    #   - produced_at (date/heure, valeur par défaut = maintenant)

    work_order: Mapped[WorkOrder] = relationship(back_populates="parts")
