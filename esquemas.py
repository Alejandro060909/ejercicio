from pydantic import BaseModel, Field, Form
from typing import Annotated


class ProductoActualizar(BaseModel):
    """Datos que el estudiante envía al editar un producto."""
    nombre: Annotated[str | None, Form()] = None,
    precio: Annotated[str | None, Form()] = None,
    cantidad: Annotated[str | None, Form()] = None,
    descripcion: Annotated[str | None, Form()] = None,



    # TODO(1): define las reglas de validación de cada campo:
    # - nombre: obligatorio, entre 1 y 100 caracteres
    # - precio: número mayor que cero
    # - cantidad: número entero, mayor o igual que cero
    # - descripcion: opcional
    pass