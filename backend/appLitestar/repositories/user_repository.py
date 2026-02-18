from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.modelsUsuarios import Usuario

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> Usuario | None:
        query = select(Usuario).where(Usuario.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Usuario]:
        result = await self.session.execute(select(Usuario))
        return result.scalars().all()

    async def get_by_roles(self, roles: list[str]) -> list[Usuario]:
        query = select(Usuario).where(Usuario.rol.in_(roles))
        result = await self.session.execute(query)
        return result.scalars().all()