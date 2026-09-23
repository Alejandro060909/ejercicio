from pydantic import BaseModel, Field


class ProductoActualizar(BaseModel):
    """Datos que el estudiante envía al editar un producto."""

    # TODO(1): define las reglas de validación de cada campo:
    # - nombre: obligatorio, entre 1 y 100 caracteres
    # - precio: número mayor que cero
    # - cantidad: número entero, mayor o igual que cero
    # - descripcion: opcional
    pass