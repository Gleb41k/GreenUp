from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.dto.user_dto import UserCreateDTO
from app.repositories.user_repository_protocol import UserRepositoryProtocol


class UserRepository(UserRepositoryProtocol):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, dto: UserCreateDTO, hashed_password: str) -> User:
        user = User(
            email=str(dto.email),
            hashed_password=hashed_password,
            full_name=dto.full_name,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
