import asyncpg


class Db:
    """Envoltorio mínimo sobre el pool de conexiones de asyncpg."""

    pool: asyncpg.Pool | None = None

    async def connect(self, DATABASE_URL: str):
        # Crea un pool: varias conexiones que se reutilizan entre peticiones.
        self.pool = await asyncpg.create_pool(dsn="postgresql://neondb_owner:npg_qgvYbXeI78EM@ep-patient-math-apihp7g4-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

    async def close(self):
        if self.pool is not None:
            await self.pool.close()
            self.pool = None


db = Db()


async def get_connection():
    """Dependencia de FastAPI: cede una conexión del pool a cada petición."""
    async with db.pool.acquire() as conn:
        yield conn