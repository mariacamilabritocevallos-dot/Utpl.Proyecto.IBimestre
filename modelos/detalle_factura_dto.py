from typing import Optional
from pydantic import BaseModel

class DetalleFactura(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float