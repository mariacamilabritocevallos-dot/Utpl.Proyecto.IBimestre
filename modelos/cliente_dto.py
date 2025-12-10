from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class Cliente(BaseModel):
    id: int
    nombre: str = Field(..., min_length=4, max_length=100, description="Nombre del cliente", examples =["Juan", "María"])
    correo: EmailStr = Field(..., description="Correo electrónico del cliente", examples =["juan.perez@example.com", "maria.gonzalez@example.com"])
    telefono: str = Field(..., min_length=7, max_length=15, description="Número de teléfono del cliente", examples=["0987654321", "+593987654321"])

    identificacion: str = Field(..., min_length=10, max_length=10, description="Identificacion del cliente", examples =["1234567891", "2345678987"])