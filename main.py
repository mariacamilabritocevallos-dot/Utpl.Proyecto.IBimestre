"""
API REST básica con FastAPI
Este es un esqueleto de API para enseñar a estudiantes
"""

from fastapi import FastAPI
from modelos.cliente_dto import Cliente
from modelos.producto_dto import Producto
from modelos.detalle_factura_dto import DetalleFactura
from modelos.factura_dto import Factura

# Crear la instancia de FastAPI
app = FastAPI(
    title="API de Facturacion- Maria Brito",
    description="API REST para la gestión de procesos de facturación",
    version="1.0.0"
)


@app.get("/")
def root():
    """
    Endpoint raíz - Hola Mundo
    """
    return {"mensaje": "¡Hola Mundo desde FastAPI!"}


@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    """
    Endpoint de ejemplo con parámetro de ruta
    """
    return {"mensaje": f"¡Hola {nombre}! Bienvenido a la API"}


@app.get("/info")
def informacion():
    """
    Endpoint de información de la API
    """
    return {
        "nombre": "API de Facturacion",
        "version": "1.0.0",
        "descripcion": "API diseñada para la gestión de procesos de facturación"
        }

@app.post("/clientes", response_model=Cliente, tags=["Clientes"])
def crear_cliente(cliente: Cliente):
    """
    Endpoint para crear un nuevo cliente
    """
    return cliente


@app.post("/productos", response_model=Producto, tags=["Productos"])
def crear_producto(producto: Producto):
    """
    Endpoint para crear un nuevo producto
    """
    return producto

@app.post("/detalle_factura", response_model=DetalleFactura, tags=["Detalle Factura"])
def crear_detalle_factura(detalle: DetalleFactura):
    """
    Endpoint para crear un nuevo detalle de factura
    """
    return detalle

@app.post("/factura", response_model=Factura, tags=["Factura"])
def crear_factura(factura: Factura):
    """
    Endpoint para crear una nueva factura
    """
    return factura
