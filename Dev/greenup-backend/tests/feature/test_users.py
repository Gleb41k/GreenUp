import pytest
from httpx import AsyncClient

from app.core.security.password import get_password_service
from app.dependencies.auth import get_current_user
from app.dependencies.repositories import get_user_repository
from app.main import app


@pytest.mark.asyncio
async def test_me_endpoint(client: AsyncClient, mocker):
    mock_user = mocker.MagicMock()
    mock_user.id = 1
    mock_user.email = "me@example.com"

    # === ПРАВИЛЬНО: используем FastAPI app ===
    async def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.get(
        "/api/v1/users/me", headers={"Authorization": "Bearer valid-token"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"

    # === ОЧИСТКА ===
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient, mocker):
    # === Создаём "реальный" объект пользователя ===
    mock_user = mocker.MagicMock()
    mock_user.id = 1
    mock_user.email = "new@example.com"
    mock_user.hashed_password = "hashed"
    mock_user.is_active = True
    mock_user.full_name = None  # ← ЯВНО str | None

    # === Мокаем репозиторий ===
    mock_repo = mocker.MagicMock()
    mock_repo.get_by_email = mocker.AsyncMock(return_value=None)
    mock_repo.create = mocker.AsyncMock(return_value=mock_user)

    # === Мокаем pwd_service ===
    mock_pwd_service = mocker.MagicMock()
    mock_pwd_service.hash.return_value = "hashed"

    # === dependency_overrides ===
    async def override_get_user_repository():
        return mock_repo

    def override_get_password_service():
        return mock_pwd_service

    app.dependency_overrides[get_user_repository] = override_get_user_repository
    app.dependency_overrides[get_password_service] = override_get_password_service

    # === Запрос ===
    response = await client.post(
        "/api/v1/users/", json={"email": "new@example.com", "password": "Secret123"}
    )

    # === Проверки ===
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["email"] == "new@example.com"
    assert data.get("full_name") is None  # ← валидируется

    # === Проверка вызовов ===
    mock_repo.create.assert_called_once()
