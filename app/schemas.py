"""Schémas Pydantic : ce que l'API reçoit et renvoie (validation automatique)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkOrderCreate(BaseModel):
    product: str
    planned_quantity: int = Field(gt=0)  # doit être > 0


class WorkOrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # lit directement un objet SQLAlchemy

    id: int
    product: str
    planned_quantity: int
    status: str
    created_at: datetime


# TODO (jour 1) : PartCreate, PartOut, OrderSummary
# TODO (jour 2) : MachineEventCreate
