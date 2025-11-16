from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # ← ВАЖНО!

    id: UUID                     # ← UUID, а не str!
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

    is_active: bool = True
    is_verified: bool = False
    is_blocked: bool = False

    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None