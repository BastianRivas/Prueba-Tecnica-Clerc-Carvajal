import os
from pathlib import Path
from aiomysql import OperationalError
from litestar import Litestar, get
from litestar.response import Redirect
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.di import Provide
from database.session import get_db, engine, Base, async_session
from controller.user_controller import AuthController
from litestar.static_files import create_static_files_router # Importante
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.config.cors import CORSConfig

# Configuración de Sesiones
# Esto guardará un ID en una cookie y los datos en el servidor
session_config = ServerSideSessionConfig(
    samesite="none",  # Permite que la cookie se envíe desde dominios distintos
    secure=True,      # Requerido para samesite="none" (Render usa HTTPS)
    httponly=True     # Seguridad básica
)
BASE_DIR = Path(__file__).parent # Esto apunta a la carpeta appLitestar

# Función para inicializar la base de datos al arrancar
async def on_startup() -> None:
    global engine # Necesitamos acceder al engine global para re-configurarlo
    
    try:
        # Intento 1: Probar la conexión actual (MySQL)
        async with engine.begin() as conn:
            print("🚀 Conexión exitosa a la base de datos principal.")
            await conn.run_sync(Base.metadata.create_all)
            
    except (OperationalError, Exception) as e:
        print(f"⚠️ Falló conexión principal: {e}")
        print("🔄 Cambiando a Modo de Respaldo (SQLite)...")
        
        # Intento 2: Reconfigurar todo para SQLite
        fallback_url = "sqlite+aiosqlite:///./test.db"
        
        # Creamos un nuevo engine de emergencia
        from sqlalchemy.ext.asyncio import create_async_engine
        new_engine = create_async_engine(fallback_url, echo=True)
        
        # Actualizamos la fábrica de sesiones para que use el nuevo engine
        async_session.configure(bind=new_engine)
        
        # Creamos las tablas en SQLite
        async with new_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Aplicación iniciada con SQLite local.")

#Para llevarlo directo a la pagina de login, se redirecciona a esa ruta desde la raiz y cualquier ruta no definida. Esto es opcional pero mejora la experiencia de usuario al no mostrar un error 404 o una página vacía.
@get("/")
async def index() -> Redirect:
    return Redirect(path="/auth/login-page")

@get("/{path:path}", include_in_schema=False)
async def redirect_all(path: str) -> Redirect:
    return Redirect(path="/auth/login-page")



# Definimos la configuración de CORS
cors_config = CORSConfig(
    allow_origins=["http://localhost:4200","https://prueba-tecnica-clerc-carvajal.vercel.app"], # Permite Angular local
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True, # Importante si usas sesiones/cookies
)

#Instancia de la Aplicación Litestar
app = Litestar(
    route_handlers=[index, redirect_all,
        AuthController,
        create_static_files_router(path="/static", directories=["static"]),
    ],
    dependencies={
        "db_session": Provide(get_db), # Inyecta la sesión de SQLAlchemy automáticamente
    },
    middleware=[session_config.middleware],
    on_startup=[on_startup],
    template_config=TemplateConfig(
        directory=BASE_DIR / "templates", # Ruta absoluta
        engine=JinjaTemplateEngine,
    ),
    cors_config=cors_config, 
)
