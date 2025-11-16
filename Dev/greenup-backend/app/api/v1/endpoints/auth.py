from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.logger import get_logger
from app.core.security.jwt import (create_access_token, create_refresh_token,
                                   verify_token)
from app.core.security.password import get_password_service
from app.dependencies.repositories import get_user_repository
from app.dto.auth_dto import LoginDTO
from app.repositories.user_repository_protocol import UserRepositoryProtocol
from app.schemas.token import TokenOut

router = APIRouter()
logger = get_logger()
pwd_service = get_password_service()


@router.post("/login", response_model=TokenOut)
async def login(
    dto: LoginDTO, repo: UserRepositoryProtocol = Depends(get_user_repository)
):
    user = await repo.get_by_email(str(dto.email))
    if not user or not pwd_service.verify(user.hashed_password, dto.password):
        logger.warning(
            "Login failed", {"email": dto.email, "reason": "invalid credentials"}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    expires_delta = timedelta(minutes=15)
    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})
    expires_at = datetime.now(UTC) + expires_delta

    logger.info("User logged in", {"user_id": user.id, "email": user.email})
    return TokenOut(access_token=access, refresh_token=refresh, expires_at=expires_at)


@router.post("/refresh", response_model=TokenOut)
async def refresh_token(refresh_token: str):
    try:
        payload = verify_token(refresh_token, "refresh")
        access = create_access_token({"sub": payload["sub"]})
        new_refresh = create_refresh_token({"sub": payload["sub"]})
        return TokenOut(access_token=access, refresh_token=new_refresh)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
