from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models.modelsUsuarios import Usuario

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(Usuario))
        return result.scalars().all()

    async def get_by_role(self, roles: list[str]):
        result = await self.session.execute(
            select(Usuario).where(Usuario.role.in_(roles))
        )
        return result.scalars().all()