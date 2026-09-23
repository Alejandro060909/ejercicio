import os

import asyncpg


class Db:
    """Envoltorio mínimo sobre el pool de conexiones de asyncpg."""

    pool: asyncpg.Pool | None = None

    async def connect(self, database_url: str | None = None):
        dsn = database_url or os.getenv("DATABASE_URL")
        if not dsn:
            raise RuntimeError("La variable de entorno DATABASE_URL no está configurada")

        # Un pool pequeño evita abrir demasiadas conexiones en funciones serverless.
        self.pool = await asyncpg.create_pool(dsn=dsn, min_size=0, max_size=5)

    async def close(self):
        if self.pool is not None:
            await self.pool.close()
            self.pool = None


db = Db()


async def get_connection():
    """Dependencia de FastAPI: cede una conexión del pool a cada petición."""
    async with db.pool.acquire() as conn:
        yield conn