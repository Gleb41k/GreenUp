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

class User(Base):
    """
    Основная таблица пользователей.
    Хранит персональные данные, статусы и метаданные.
    """
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("phone", name="uq_users_phone"),
        {"comment": "Таблица зарегистрированных пользователей"},
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Уникальный UUID"
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, comment="Email (уникальный)"
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, unique=True, comment="Телефон (опционально, уникальный)"
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Хэшированный пароль (Argon2)"
    )

    full_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="ФИО"
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(512), nullable=True, comment="URL аватара"
    )

    # Статусы
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, comment="Активен ли аккаунт"
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Подтверждён ли email"
    )
    is_blocked: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Заблокирован ли"
    )

    # Метаданные
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), comment="Дата регистрации"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        comment="Дата обновления"
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="Последний вход"
    )

    # Связи
    tokens: Mapped[list["VerificationToken"]] = relationship(
        "VerificationToken", back_populates="user", cascade="all, delete-orphan"
    )
    password_resets: Mapped[list["PasswordResetToken"]] = relationship(
        "PasswordResetToken", back_populates="user", cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        """Хэширует и сохраняет пароль"""
        self.hashed_password = get_password_service().hash(password)

    def check_password(self, password: str) -> bool:
        """Проверяет пароль"""
        return get_password_service().verify(self.hashed_password, password)



