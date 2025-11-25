from typing import Optional
from pydantic import BaseModel

class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio_unitario: float
    stock: int