from __future__ import annotations

from datetime import datetime, UTC
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    String, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.base import Base
from app.core.security.password import get_password_service

class VerificationToken(Base):
    """
    Токены для подтверждения email и телефона
    """
    __tablename__ = "verification_tokens"
    __table_args__ = (
        UniqueConstraint("token", name="uq_verification_token"),
        {"comment": "Токены подтверждения регистрации"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    token_type: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="email_verify | phone_verify"
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, comment="Истекает через 15 минут"
    )
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    user: Mapped["User"] = relationship("User", back_populates="tokens")

