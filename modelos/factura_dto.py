from typing import Optional, List
from datetime import date
from pydantic import BaseModel

from modelos.detalle_factura_dto import DetalleFactura  # IMPORTANTE

class Factura(BaseModel):
    id: int
    cliente_id: int
    fecha: date
    detalles: List[DetalleFactura]
    subtotal: float
    impuesto: float
    total: float