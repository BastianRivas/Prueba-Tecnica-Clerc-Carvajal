from litestar import Litestar, get, post, Request, Response
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.datastructures import State
from litestar.status_codes import HTTP_401_UNAUTHORIZED

# Configuración de sesión simple en memoria (o puedes usar Redis/DB)
session_config = ServerSideSessionConfig()

@post("/login")
async def login(request: Request, data: dict, db_session: AsyncSession) -> dict:
    # 1. Buscar usuario en DB
    # 2. Validar contraseña (usa passlib para el hash)
    # 3. Guardar en sesión
    request.set_session({"user_id": user.id, "role": user.role})
    return {"message": "Login exitoso"}

@get("/api/data")
async def get_users(request: Request, db_session: AsyncSession) -> list:
    user_id = request.session.get("user_id")
    if not user_id:
        return Response(content={"error": "No autorizado"}, status_code=HTTP_401_UNAUTHORIZED)
    
    # Obtener el objeto del usuario actual
    current_user = await db_session.get(User, user_id)
    
    # Aplicar la lógica de roles definida arriba
    users = await get_visible_users(db_session, current_user)
    
    return [{"username": u.username, "role": u.role, "email": u.email} for u in users]

def create_app():
    return Litestar(
        route_handlers=[login, get_users],
        middleware=[session_config.middleware],
        state=State(get_initial_state()),
    )