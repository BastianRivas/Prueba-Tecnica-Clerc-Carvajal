from litestar import Controller, get, post, Request, Response
from litestar.status_codes import HTTP_401_UNAUTHORIZED
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.modelsUsuarios import Usuario
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from litestar.response import Template
from litestar.template.config import TemplateConfig

class AuthController(Controller):
    path = "/auth"

    @post("/login")
    async def login(self, request: Request, data: dict, db_session: AsyncSession) -> dict:
        repo = UserRepository(db_session)
        service = AuthService(repo)
        
        user = await service.authenticate(data["username"], data["password"])

        if not user:
            print(f"❌ Usuario no encontrado: {user}")
        else:
            # Si el usuario existe, el problema es la contraseña
            print(f"✅ Usuario encontrado: {user.username}")
        print(f"🔑 Verificando contraseña...")
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
            return Response({"error": "No logueado"}, status_code=HTTP_401_UNAUTHORIZED)
            
        repo = UserRepository(db_session)
        service = AuthService(repo)
        
        # Obtenemos al usuario actual para saber su rol
        current_user = await db_session.get(Usuario, user_id)
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