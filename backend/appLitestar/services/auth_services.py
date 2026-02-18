# Lógica simple de autenticación (ejemplo)
# Implementa según necesidades reales (tokens, sesiones, hashes)

import json
from pathlib import Path
from typing import Optional
from passlib.context import CryptContext

DATA_FILE = Path(__file__).parent / "data" / "datosBrutos.json"


# Configuración del esquema de hasheo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

