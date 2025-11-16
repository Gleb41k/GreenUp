from app.core.logger.factory import get_logger
from app.core.security.password import get_password_service
from app.dto.user_dto import UserCreateDTO
from app.repositories.user_repository_protocol import UserRepositoryProtocol
from app.tasks.tasks import send_welcome_email

logger = get_logger()


async def create_user(
    dto: UserCreateDTO, repo: UserRepositoryProtocol, pwd_service=get_password_service()
):
    logger.info("Creating user", context={"email": str(dto.email)})
    if await repo.get_by_email(str(dto.email)):
        raise ValueError("Email already registered")

    hashed = pwd_service.hash(dto.password)
    user = await repo.create(dto, hashed)
    send_welcome_email.delay(user.email)
    return user
