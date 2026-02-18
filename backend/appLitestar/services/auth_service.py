# Lógica simple de autenticación (ejemplo)
# Implementa según necesidades reales (tokens, sesiones, hashes)

import json
from pathlib import Path
from typing import Optional
from passlib.context import CryptContext
from repositories.user_repository import UserRepository
from database.models.modelsUsuarios import Usuario

DATA_FILE = Path(__file__).parent / "data" / "datosBrutos.json"


# Configuración del esquema de hasheo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def authenticate(self, username: str, password: str) -> Optional[Usuario]:
        user = await self.repository.get_by_username(username)
        if user and pwd_context.verify(password[:72], user.password):
            return user
        return None

    async def get_visible_data(self, current_user: Usuario) -> list[Usuario]:
        """Aplica las reglas de negocio de la prueba técnica"""
        if current_user.rol == "admin":
            return await self.repository.get_all()
            
        if current_user.rol == "supervisor":
            # Puede ver supervisores y usuarios
            return await self.repository.get_by_roles(["supervisor", "usuario"])
            
        # Rol 'usuario': solo se ve a sí mismo
        return [current_user]


def hash_password(password: str) -> str:
    # Bcrypt solo acepta hasta 72 caracteres, truncamos por seguridad y para evitar errores
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password[:72], hashed_password)
    except Exception:
        return False

def load_users() -> list:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def authenticate(username: str, password: str) -> Optional[dict]:
    users = load_users()
    for u in users:
        if u.get("username") == username and u.get("password") == password:
            return u
    return None

