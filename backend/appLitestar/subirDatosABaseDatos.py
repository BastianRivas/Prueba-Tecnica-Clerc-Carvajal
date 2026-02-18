import asyncio
import json
import os
from sqlalchemy.future import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine

# Importamos tus componentes
from database.session import async_session, engine, Base, DATABASE_URL
from database.models.modelsUsuarios import Usuario
from services.auth_service import hash_password

async def seed_data():
    global engine
    print(f"🚀 Iniciando proceso de carga...")

    # --- LÓGICA DE RESCATE (Igual que en tu App) ---
    try:
        # Intentamos conectar a MySQL
        async with engine.begin() as conn:
            print("🔗 Conectado a MySQL exitosamente.")
            await conn.run_sync(Base.metadata.create_all)
    except (OperationalError, Exception) as e:
        print(f"⚠️ MySQL no disponible ({e}).")
        print("🔄 Cambiando a Modo de Respaldo: SQLite (test.db)...")
        
        # Creamos engine de respaldo
        fallback_url = "sqlite+aiosqlite:///./test.db"
        engine = create_async_engine(fallback_url, echo=True)
        
        # Re-configuramos la sesión para que use el nuevo engine
        async_session.configure(bind=engine)
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # --- PROCESO DE CARGA DE DATOS ---
    async with async_session() as db:
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'datosBrutos.json')
        
        if not os.path.exists(file_path):
            print(f"❌ Error: No se encontró el archivo en {file_path}")
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        for u in raw_data:
            # Generar username automáticamente si no existe
            username = u.get("username", u["nombre"].lower().replace(" ", "_"))
            
            result = await db.execute(select(Usuario).filter(Usuario.nombre == u["nombre"]))
            exists = result.scalars().first()

            if not exists:
                print(f"➕ Insertando: {u['nombre']}")
                nuevo_usuario = Usuario(
                    id=u["id"],
                    nombre=u["nombre"],
                    rol=u["rol"],
                    renta_mensual=u["renta_mensual"],
                    username=username,
                    password=hash_password("12345")
                )
                db.add(nuevo_usuario)
            else:
                print(f"⏩ Saltando {u['nombre']}, ya existe.")

        await db.commit()
        print("\n✨ ¡Carga completada con éxito!")

if __name__ == "__main__":
    try:
        asyncio.run(seed_data())
    except Exception as e:
        print(f"💥 Error crítico en el script: {e}")