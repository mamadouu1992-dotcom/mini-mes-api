"""Schémas Pydantic : ce que l'API reçoit et renvoie (validation automatique)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, typing
from typing import Literal

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

class PartCreate(BaseModel):
    serial_number: str
    quality_result: Literal["GOOD", "REJECTED"]


class PartOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    work_order_id: int
    serial_number: str
    quality_result: str
    produced_at: datetime

class OrderSummary(BaseModel):

    order_id: int
    total_parts: int
    good_parts: int
    rejected_parts: int
    yield_percent: float

# TODO (jour 2) : MachineEventCreate


