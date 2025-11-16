from datetime import UTC, datetime
from typing import Awaitable, Callable

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.models.user import User
from app.db.session import get_db
from app.core.security.jwt import verify_token


class LastLoginMiddleware(BaseHTTPMiddleware):
    """
    Обновляет поле last_login_at при успешной авторизации (валидный JWT)
    """
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Пропускаем не-API роуты и OPTIONS
        if not request.url.path.startswith("/api/") or request.method == "OPTIONS":
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return await call_next(request)

        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token)
            user_id = payload.get("sub")
            if not user_id:
                return await call_next(request)

            # Получаем сессию из dependency (или создаём временную)
            session: AsyncSession = request.state.db if hasattr(request.state, "db") else get_db()

            async with session.begin():
                user = await session.get(User, user_id)
                if user and not user.is_blocked:
                    user.last_login_at = datetime.now(UTC)
                    await session.commit()

        except Exception as e:
            # Не ломаем запрос, если что-то пошло не так
            print(f"LastLoginMiddleware error: {e}")

        return await call_next(request)