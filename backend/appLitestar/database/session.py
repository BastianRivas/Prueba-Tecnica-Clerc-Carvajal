import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DB_STATUS = "🟢 Producción (MySQL/Postgres)"

if not DATABASE_URL:
    DATABASE_URL = "sqlite+aiosqlite:///./test.db"
    DB_STATUS = "🟡 Modo de Respaldo (SQLite Local)"

# 1. Crear el engine asíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# 2. Configurar la fábrica de sesiones asíncronas
async_session = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

Base = declarative_base()

# 3. Función para obtener la base de datos (Dependencia para Litestar)
async def get_db():
    async with async_session() as session:
        yield session

def get_initial_state() -> dict:
    return {"db_status": DB_STATUS}