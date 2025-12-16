"""
API REST básica con FastAPI
Implementación base de una API orientada a la gestión de facturación.
"""

from fastapi import FastAPI, HTTPException
from modelos.cliente_dto import Cliente
from modelos.producto_dto import Producto
from modelos.detalle_factura_dto import DetalleFactura
from modelos.factura_dto import Factura
from db.supabase import create_supabase_client

# Simulación de base de datos
dbClientes = []
dbProductos = []
dbDetalles = []
dbFacturas = []

#Crear el cliente de Supabase
supabase = create_supabase_client()

# Descripción completa de la API con Markdown
descriptionInfo = """
## API REST 
Esta API REST fue desarrollada con FastAPI para gestionar procesos de facturación, permitiendo la interoperabilidad entre sistemas y el manejo eficiente de la información.
 
 Funcionalidades principales:

Gestión de Facturación:
- Se pueden realizar operaciones CRUD completas:
- Crear nuevas facturas con validación de datos
- Consultar todas las facturas o buscar por número de factura o identificación del cliente
- Actualizar información de facturas existentes
- Eliminar registros de facturas

Gestión de Clientes:
-Registrar clientes
- Consultar información de clientes
- Actualizar datos de clientes
- Eliminar registros de clientes
 
 Base de Datos:
- Integración con Supabase como backend
- Validación automática de datos con Pydantic
- Manejo de errores mediante códigos HTTP 
"""

# Instancia de FastAPI
app = FastAPI(
    title="API de Facturación - Maria Brito - mcbrito6@utpl.edu.ec",
    description= descriptionInfo,
    version="1.0.0"
)


# ROOT Y ENDPOINTS BÁSICOS


@app.get("/")
def root():
    """Endpoint raíz - Hola Mundo"""
    return {"mensaje": "¡Hola Mundo desde FastAPI!"}


@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    """Endpoint de ejemplo con parámetro de ruta"""
    return {"mensaje": f"¡Hola {nombre}! Bienvenido a la API"}


@app.get("/info")
def informacion():
    """Información general de la API"""
    return {
        "nombre": "API de Facturación",
        "version": "1.0.0",
        "descripcion": "API diseñada para la gestión de procesos de facturación"
    }

# ==================   CLIENTES   ======================


@app.post("/clientes", response_model=Cliente, tags=["Clientes"])
def crear_cliente(cliente: Cliente):
    """Crear un nuevo cliente"""

    data = supabase.table("cliente").insert({
        "nombre": cliente.nombre,
        "correo": cliente.correo,
        "telefono": cliente.telefono

        }).execute()
    return cliente


@app.get("/clientes", response_model=list[Cliente], tags=["Clientes"])
def obtener_clientes():
    """Obtener todos los clientes"""
    data = supabase.table("cliente").select("*").execute()
    return data.data


@app.get("/clientes/{identificacion}", response_model=Cliente, tags=["Clientes"])
def obtener_cliente_por_identificacion(identificacion: str):
    """Buscar un cliente por su identificación"""
    data = supabase.table("cliente").select("*").eq("identificacion", identificacion).execute()
    if data.data:
        return data.data[0]
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


@app.put("/clientes/{identificacion}", response_model=Cliente, tags=["Clientes"])
def actualizar_cliente(identificacion: str, cliente_actualizado: Cliente):
    """
    Actualizar un cliente existente.
    La identificación del cuerpo debe coincidir con la de la ruta.
    """
    if cliente_actualizado.identificacion != identificacion:
        raise HTTPException(status_code=400, detail="Identificación inconsistente")

    data = supabase.table("cliente").update({
        "nombre": cliente_actualizado.nombre,
        "correo": cliente_actualizado.correo,
        "telefono": cliente_actualizado.telefono
        }).eq("identificacion", identificacion).execute()
    if data.data:
        return cliente_actualizado

    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.delete("/clientes/{identificacion}", response_model=Cliente, tags=["Clientes"])
def eliminar_cliente(identificacion: str):
    """Eliminar un cliente por su identificación.
    Retorna el cliente eliminado o 404 si no existe.
    """
    data = supabase.table("cliente").delete().eq("identificacion", identificacion).execute()
    if data.data:
        return data.data[0]
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# ==================   PRODUCTOS   =====================


@app.post("/productos", response_model=Producto, tags=["Productos"])
def crear_producto(producto: Producto):
    """Crear un nuevo producto"""
    dbProductos.append(producto)
    return producto


@app.get("/productos", response_model=list[Producto], tags=["Productos"])
def obtener_productos():
    """Obtener todos los productos"""
    return dbProductos


@app.get("/productos/{codigo}", response_model=Producto, tags=["Productos"])
def obtener_producto_por_codigo(codigo: str):
    """Buscar un producto por código"""
    for p in dbProductos:
        if p.codigo == codigo:
            return p
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.put("/productos/{codigo}", response_model=Producto, tags=["Productos"])
def actualizar_producto(codigo: str, producto_actualizado: Producto):
    """Actualizar un producto por código"""
    if producto_actualizado.codigo != codigo:
        raise HTTPException(status_code=400, detail="Código inconsistente")

    for idx, p in enumerate(dbProductos):
        if p.codigo == codigo:
            dbProductos[idx] = producto_actualizado
            return producto_actualizado

    raise HTTPException(status_code=404, detail="Producto no encontrado")


# ================= DETALLE FACTURA ====================


@app.post("/detalle_factura", response_model=DetalleFactura, tags=["Detalle Factura"])
def crear_detalle_factura(detalle: DetalleFactura):
    """Crear detalle de factura"""
    dbDetalles.append(detalle)
    return detalle


@app.get("/detalle_factura", response_model=list[DetalleFactura], tags=["Detalle Factura"])
def obtener_detalles_factura():
    """Obtener todos los detalles de factura"""
    return dbDetalles


# ===================== FACTURA ========================


@app.post("/factura", response_model=Factura, tags=["Factura"])
def crear_factura(factura: Factura):
    """Crear una nueva factura"""
    dbFacturas.append(factura)
    return factura


@app.get("/factura", response_model=list[Factura], tags=["Factura"])
def obtener_facturas():
    """Obtener todas las facturas"""
    return dbFacturas


@app.get("/factura/{id}", response_model=Factura, tags=["Factura"])
def obtener_factura_por_id(id: int):
    """Buscar una factura por ID"""
    for f in dbFacturas:
        if f.id == id:
            return f
    raise HTTPException(status_code=404, detail="Factura no encontrada")


@app.put("/factura/{id}", response_model=Factura, tags=["Factura"])
def actualizar_factura(id: int, factura_actualizada: Factura):
    """Actualizar una factura por ID"""
    if factura_actualizada.id != id:
        raise HTTPException(status_code=400, detail="El ID del cuerpo no coincide con la ruta")

    for idx, f in enumerate(dbFacturas):
        if f.id == id:
            dbFacturas[idx] = factura_actualizada
            return factura_actualizada

    raise HTTPException(status_code=404, detail="Factura no encontrada")
