from pathlib import Path
from typing import Annotated
from pydantic import ValidationError
from esquemas import ProductoActualizar

from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from dependencias import ConnectionDep
from repositorio import actualizar_producto, obtener_producto, obtener_productos

router = APIRouter(tags=["productos"])

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@router.get("/productos")
async def listar_productos(request: Request, conn: ConnectionDep):
    # Ya implementado: muestra la página con la lista de productos.
    productos = await obtener_productos(conn)
    return templates.TemplateResponse(
        request=request,
        name="productos.html",
        context={"productos": productos},
    )


@router.get("/productos/{producto_id}/editar")
async def editar_producto_vista(request: Request, conn: ConnectionDep, producto_id: int):
    producto = await obtener_producto(conn, producto_id)
    if producto is None:
        return templates.TemplateResponse(
            request=request,
            name="componentes/producto_no_encontrado.html",
            context={"producto_id": producto_id},
        )
    return templates.TemplateResponse(
        request=request,
        name="componentes/fila_editar.html",
        context={
            "producto": producto,
            "nombre": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": producto["cantidad"],
            "descripcion": producto["descripcion"],
            "errores": {},
        },
    )


@router.get("/productos/{producto_id}/cancelar")
async def cancelar_edicion_vista(request: Request, conn: ConnectionDep, producto_id: int):
    # Cancelar solo vuelve a mostrar la fila original, sin modificar nada.
    producto = await obtener_producto(conn, producto_id)
    if producto is None:
        return templates.TemplateResponse(
            request=request,
            name="componentes/producto_no_encontrado.html",
            context={"producto_id": producto_id},
        )
    return templates.TemplateResponse(
        request=request,
        name="componentes/fila_producto.html",
        context={"producto": producto},
    )


@router.post("/productos/{producto_id}")
async def guardar_producto_vista(
    request: Request,
    conn: ConnectionDep,
    producto_id: int,
    nombre: Annotated[str, Form()] = "",
    precio: Annotated[str, Form()] = "",
    cantidad: Annotated[str, Form()] = "",
    descripcion: Annotated[str | None, Form()] = None,
):
    # TODO(6): este es el corazón del ejercicio. Pasos a seguir:
    # 1. Convierte precio y cantidad a número (float / int).
    # 2. Valida los datos con el esquema ProductoActualizar.
    # 3. Si hay errores, vuelve a mostrar el formulario con los valores
    #    que el usuario escribió y los mensajes de error (HTTP 422).
    # 4. Si los datos son válidos, ejecuta actualizar_producto() y
    #    responde con la plantilla "componentes/fila_actualizada.html".
    producto = await obtener_producto(conn, producto_id)
    if producto is None:
        return templates.TemplateResponse(
            request=request,
            name="componentes/producto_no_encontrado.html",
            context={"producto_id": producto_id},
        )

    errores = {}

    try:
        precio_validado = float(precio)
    except (TypeError, ValueError):
        precio_validado = precio
        errores["precio"] = "El precio debe ser un número válido."

    try:
        cantidad_validada = int(cantidad)
    except (TypeError, ValueError):
        cantidad_validada = cantidad
        errores["cantidad"] = "La cantidad debe ser un número entero válido."

    producto_validado = None
    try:
        producto_validado = ProductoActualizar(
            nombre=nombre,
            precio=precio_validado,
            cantidad=cantidad_validada,
            descripcion=descripcion,
        )
    except ValidationError as exc:
        for error in exc.errors():
            campo = error["loc"][0]
            errores.setdefault(campo, error["msg"])

    if errores:
        return templates.TemplateResponse(
            request=request,
            name="componentes/fila_editar.html",
            context={
                "producto": producto,
                "nombre": nombre,
                "precio": precio,
                "cantidad": cantidad,
                "descripcion": descripcion,
                "errores": errores,
            },
            status_code=422,
        )

    await actualizar_producto(
        conn,
        producto_id,
        producto_validado.nombre,
        producto_validado.precio,
        producto_validado.cantidad,
        producto_validado.descripcion,
    )
    producto_actualizado = await obtener_producto(conn, producto_id)

    if producto_actualizado is None:
        return templates.TemplateResponse(
            request=request,
            name="componentes/producto_no_encontrado.html",
            context={"producto_id": producto_id},
        )

    return templates.TemplateResponse(
        request=request,
        name="componentes/fila_actualizada.html",
        context={"producto": producto_actualizado},
    )