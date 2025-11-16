from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security.jwt import verify_token
from app.dependencies.repositories import get_user_repository
from app.repositories.user_repository_protocol import UserRepositoryProtocol

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    repo: UserRepositoryProtocol = Depends(get_user_repository),
):
    try:
        payload = verify_token(credentials.credentials)
        user_id = int(payload["sub"])
        user = await repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return user
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
