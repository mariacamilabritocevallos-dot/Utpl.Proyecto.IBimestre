from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Factura(BaseModel):
    id: int
    cliente_id: int = Field(
        ...,
        description="Identificador del cliente al que pertenece la factura",
        examples=[1, 5]
    )
    fecha: datetime = Field(
        ...,
        description="Fecha y hora de emisión de la factura",
        examples=["2025-01-15T10:30:00"]
    )
    numero_factura: Optional[str] = Field(
        None,  # opcional
        min_length=5,
        max_length=20,
        description="Número único de la factura",
        examples=["FAC-001", "FAC-2025-10"]
    )
    total: float = Field(
        ...,
        gt=0,
        description="Total de la factura (suma de los subtotales)",
        examples=[980.49, 1250.00]
    )
