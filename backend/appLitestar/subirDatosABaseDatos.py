import asyncio
import json
import os
from sqlalchemy.future import select
# Importa tus componentes desde donde los tengas definidos
from database.session import async_session, engine, Base
from database.models.modelsUsuarios import Usuario
from backend.appLitestar.services.auth_service import hash_password

async def seed_data():
    print(f"🚀 Conectando a la DB de forma asíncrona...")
    
    # Crear tablas si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        # Cargar JSON
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'datosBrutos.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        for u in raw_data:
            username = u["nombre"].lower().replace(" ", "_")
            
            # Consulta asíncrona
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
        # Ejecutar el bucle asíncrono
        asyncio.run(seed_data())
    except Exception as e:
        print(f"💥 Error grave: {e}")
    
    # ESTO EVITA QUE LA VENTANA SE CIERRE SOLA
    input("\nPresiona ENTER para cerrar esta ventana...")