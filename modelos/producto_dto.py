from pydantic import BaseModel, Field
from typing import Optional

class Producto(BaseModel):
    id: Optional[int] = None
    codigo: str = Field(..., min_length=3, max_length=20)
    nombre: str
    descripcion: Optional[str] = None
    precio_unitario: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
