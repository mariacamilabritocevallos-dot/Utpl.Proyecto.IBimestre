from pydantic import BaseModel, Field
from typing import Optional

class DetalleFactura(BaseModel):
    id: int
    factura_id: int = Field(..., description="Identificador de la factura", examples=[1, 20])
    producto_id: Optional[int] = Field(None, description="Identificador del producto", examples=[100, 205])
    descripcion: str = Field(..., min_length=3, max_length=200, description="Descripción del producto", examples=["Camarón blanco congelado 20/30", "Atún en lomos congelado grado exportación"])
    cantidad: int = Field(..., gt=0, description="Cantidad del producto", examples=[10, 50])
    precio_unitario: float = Field(..., gt=0, description="Precio unitario", examples=[120.75, 98.50])
    subtotal: float = Field(..., gt=0, description="Subtotal", examples=[1207.50, 4925.00])
