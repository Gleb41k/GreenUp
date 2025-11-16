from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.user_repository_protocol import UserRepositoryProtocol


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepositoryProtocol:
    return UserRepository(db)
