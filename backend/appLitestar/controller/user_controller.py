

from litestar import Controller, get, post, Request, Response
from litestar.status_codes import HTTP_401_UNAUTHORIZED
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.modelsUsuarios import Usuario
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from litestar.response import Template
from litestar.response import Redirect    
from litestar.exceptions import HTTPException

class AuthController(Controller):
    path = "/auth"

    @post("/login")
    async def login(self, request: Request, data: dict, db_session: AsyncSession) -> dict:
        repo = UserRepository(db_session)
        service = AuthService(repo)
        
        user = await service.authenticate(data["username"], data["password"])
        if not user:
            return Response({"error": "Credenciales inválidas"}, status_code=HTTP_401_UNAUTHORIZED)
        
        # Guardamos el ID en la sesión de Litestar
        request.set_session({"user_id": user.id})
        return {
            "message": "success",
            "nombre": user.nombre, 
            "rol": user.rol
        }
    
    @get("/login-page")
    async def login_page(self, request: Request) -> Template: 
        return Template(template_name="index.html")


    @get("/data")
    async def get_table_data(self, request: Request, db_session: AsyncSession) -> list:
        user_id = request.session.get("user_id")
        
        if not user_id:
            # IMPORTANTE: No redirigir, lanzar excepción para que Angular la capture
            raise HTTPException(detail="No autenticado", status_code=HTTP_401_UNAUTHORIZED)
            
        repo = UserRepository(db_session)
        service = AuthService(repo)
        
        current_user = await db_session.get(Usuario, user_id)
        # Si por alguna razón el ID existe en sesión pero no en DB
        if not current_user:
            raise HTTPException(detail="Usuario no encontrado", status_code=HTTP_401_UNAUTHORIZED)

        users = await service.get_visible_data(current_user)
        
        return [
            {"nombre": u.nombre, "rol": u.rol, "renta": u.renta_mensual} 
            for u in users
        ]
    @post("/logout")
    async def logout(self, request: Request) -> dict:
        # Esta línea es la que destruye la sesión en el servidor
        request.clear_session()
        return {"message": "Sesión cerrada correctamente"}