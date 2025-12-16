from pydantic import BaseModel, Field
from typing import Optional

class DetalleFactura(BaseModel):
    factura_id: int = Field(..., description="ID de la factura")
    descripcion: str = Field(..., min_length=3, max_length=200)
    cantidad: int = Field(..., gt=0)
    precio_unitario: float = Field(..., gt=0)
