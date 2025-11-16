from datetime import datetime

from pydantic import BaseModel


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"  # → "2025-11-05T18:00:00Z"
        }
