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
    data = supabase.table("producto").insert({
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio_unitario": producto.precio_unitario,
        "stock": producto.stock
    }).execute()

    return data.data[0]

@app.get("/productos", response_model=list[Producto], tags=["Productos"])
def obtener_productos():
    data = supabase.table("producto").select("*").execute()
    return data.data

@app.get("/productos/{identificacion}", tags=["Productos"])
def obtener_producto_por_identificacion(identificacion: int):
    data = supabase.table("producto") \
        .select("*") \
        .eq("identificacion", identificacion) \
        .execute()

    print("Identificacion:", identificacion)
    print("Data:", data.data)

    if data.data:
        return data.data[0]

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


@app.post("/detalle-factura", tags=["Detalle Factura"])
def crear_detalle_factura(detalle: DetalleFactura):

    #  Verificar que la factura exista
    factura = supabase.table("factura") \
        .select("id") \
        .eq("id", detalle.factura_id) \
        .execute()

    if not factura.data:
        raise HTTPException(
            status_code=400,
            detail="La factura no existe"
        )

    #  Calcular subtotal
    subtotal = round(detalle.cantidad * detalle.precio_unitario, 2)

    insert_data = {
    "factura_id": detalle.factura_id,
    "descripcion": detalle.descripcion,
    "cantidad": detalle.cantidad,
    "precio_unitario": detalle.precio_unitario,
    "subtotal": subtotal
}


    data = supabase.table("detalle_factura").insert(insert_data).execute()

    return data.data[0]

@app.get("/detalle_factura", response_model=list[DetalleFactura], tags=["Detalle Factura"])
def obtener_detalles_factura():
    """Obtener todos los detalles de factura desde Supabase"""
    data = supabase.table("detalle_factura").select("*").execute()
    return data.data 

# ===================== FACTURA ========================


@app.post("/factura", tags=["Factura"])
def crear_factura(factura: Factura):

    # Subtotal enviado por el cliente
    subtotal = factura.subtotal

    # Calcular impuesto (IVA 12%)
    impuesto = round(subtotal * 0.12, 2)

    # Calcular total
    total = round(subtotal + impuesto, 2)

    #  Datos a insertar
    insert_data = {
        "cliente_id": factura.cliente_id,
        "fecha": factura.fecha.isoformat(),
        "subtotal": subtotal,
        "impuesto": impuesto,
        "total": total
    }

   
    if factura.numero_factura:
        insert_data["numero_factura"] = factura.numero_factura

  
    data = supabase.table("factura").insert(insert_data).execute()

    return data.data[0]


@app.get("/factura", response_model=list[Factura], tags=["Factura"])
def obtener_facturas():
    data = supabase.table("factura").select("*").execute()
    return data.data


@app.get("/factura/{identificacion}", tags=["Factura"])
def obtener_factura_por_identificacion(identificacion: str):
    data = supabase.table("factura") \
        .select("*") \
        .eq("identificacion", identificacion) \
        .execute()

    print("Identificacion recibida:", identificacion)
    print("Resultado Supabase:", data.data)

    if data.data:
        return data.data[0]

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
