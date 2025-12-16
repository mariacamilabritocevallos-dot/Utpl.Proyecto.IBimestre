from typing import Optional
from pydantic import BaseModel, Field


class Producto(BaseModel):
    id: int
    nombre: str = Field(
        ...,
        min_length=4,
        max_length=100,
        description="Nombre del producto",
        examples=["Camarón blanco congelado", "Atún en lomos"]
    )
    descripcion: Optional[str] = Field(
        None,
        min_length=10,
        max_length=200,
        description="Descripción del producto",
        examples=[
            "Camarón blanco congelado calibre 20/30, calidad exportación",
            "Atún en lomos congelado grado exportación"
        ]
    )
    precio_unitario: float = Field(
        ...,
        gt=0,
        description="Precio unitario del producto",
        examples=[120.75, 98.50]
    )
    stock: int = Field(
        ...,
        ge=0,
        description="Cantidad disponible en inventario",
        examples=[100, 500]
    )
