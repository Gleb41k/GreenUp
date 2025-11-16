from typing import Optional, Protocol

from app.db.models.user import User
from app.dto.user_dto import UserCreateDTO


class UserRepositoryProtocol(Protocol):
    async def get_by_email(self, email: str) -> Optional[User]: ...
    async def create(self, dto: UserCreateDTO, hashed_password: str) -> User: ...
    async def get_by_id(self, user_id: int) -> Optional[User]: ...
