import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Creamos el engine inicial
engine = create_async_engine(DATABASE_URL, echo=True)

# Usamos una función para generar la sesión que use el engine actual
async_session = sessionmaker(expire_on_commit=False, class_=AsyncSession)
async_session.configure(bind=engine)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session

def get_initial_state() -> dict:
    return {"db_status": "🟢 Conectado a la base de datos"}