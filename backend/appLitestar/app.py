import os
from pathlib import Path
from litestar import Litestar, get
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.di import Provide
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

# Importamos tus componentes (ajusta las rutas según tu estructura de carpetas)
from database.session import get_db, engine, Base
from controller.user_controller import AuthController
from litestar.static_files import create_static_files_router # Importante
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
# 1. Configuración de Sesiones (Requisito: Gestión de sesiones)
# Esto guardará un ID en una cookie y los datos en el servidor
session_config = ServerSideSessionConfig()
BASE_DIR = Path(__file__).parent # Esto apunta a la carpeta appLitestar
# 2. Función para inicializar la base de datos al arrancar
async def on_startup() -> None:
    async with engine.begin() as conn:
        # Crea las tablas si no existen
        await conn.run_sync(Base.metadata.create_all)

# 3. Instancia de la Aplicación Litestar
app = Litestar(
    route_handlers=[
        AuthController,
        create_static_files_router(path="/static", directories=["static"]),
        # UserController, # Aquí añadirías más controladores si los separas
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
    # Para que el frontend pueda acceder (CORS) si fuera necesario
    cors_config=None, 
)
