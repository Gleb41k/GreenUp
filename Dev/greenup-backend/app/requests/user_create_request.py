from pydantic import BaseModel

from app.core.logger.factory import get_logger
from app.dto.user_dto import UserCreateDTO

logger = get_logger()


class UserCreateRequest(BaseModel):
    email: str
    password: str
    full_name: str | None = None

    def to_dto(self) -> UserCreateDTO:
        logger.debug("Mapping to DTO", context={"email": self.email})
        return UserCreateDTO(**self.model_dump())
