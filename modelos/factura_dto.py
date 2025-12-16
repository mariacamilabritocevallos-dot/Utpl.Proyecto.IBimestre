from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Factura(BaseModel):
    cliente_id: int = Field(..., description="ID del cliente")
    fecha: datetime = Field(..., description="Fecha y hora de emisión")
    numero_factura: Optional[str] = Field(None, min_length=5, max_length=20)
    subtotal: float = Field(..., gt=0, description="Subtotal de la factura")
