import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Cargar variables del archivo .env
load_dotenv()

# --- CONFIGURACIÓN DE CONEXIÓN ---
DATABASE_URL = os.getenv("DATABASE_URL")
DB_STATUS = "🟢 Producción (MySQL/Postgres)"

if not DATABASE_URL:
    # Nota: Para Litestar/Async preferimos aiosqlite
    DATABASE_URL = "sqlite+aiosqlite:///./test.db"
    DB_STATUS = "🟡 Modo de Respaldo (SQLite Local)"

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# --- PASAR EL ESTADO A LA APP ---
def get_initial_state() -> dict:
    return {"db_status": DB_STATUS}
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()