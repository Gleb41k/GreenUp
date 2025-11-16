from fastapi import APIRouter, Depends, status

from app.core.security.password import get_password_service
from app.db.models import User
from app.dependencies.auth import get_current_user
from app.dependencies.repositories import get_user_repository
from app.repositories.user_repository import UserRepository
from app.requests.user_create_request import UserCreateRequest
from app.schemas.user import UserOut
from app.services.user_service import create_user

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserCreateRequest,
    repo: UserRepository = Depends(get_user_repository),
    pwd_service=get_password_service(),
):
    dto = request.to_dto()
    user = await create_user(dto, repo, pwd_service)
    return UserOut.model_validate(user)


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}
