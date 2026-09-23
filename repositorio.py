# Este archivo concentra todas las consultas SQL del ejercicio.
# Todas usan parámetros ($1, $2, ...): nunca se concatenan valores
# recibidos del formulario dentro del texto SQL.


async def obtener_productos(conn) -> list[dict]:
    """Devuelve todos los productos, ordenados por nombre."""
    # TODO(2): escribe la consulta SELECT y convierte las filas a dicts.
    ...


async def obtener_producto(conn, producto_id: int) -> dict | None:
    """Busca un producto por su clave primaria (id)."""
    # TODO(3): escribe la consulta SELECT con el parámetro $1.
    ...


async def actualizar_producto(
    conn,
    producto_id: int,
    nombre: str,
    precio: float,
    cantidad: int,
    descripcion: str | None,
) -> bool:
    """Actualiza un producto identificado por su clave primaria (id).

    Devuelve True si la consulta modificó una fila, False si no existía.
    """
    # TODO(4): escribe la consulta UPDATE parametrizada.
    # Pista: asyncpg devuelve "UPDATE 1" si modificó una fila.
    ...