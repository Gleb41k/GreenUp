import pytest
from httpx import AsyncClient

from app.core.security.password import get_password_service
from tests.factories.user_factory import UserFactory


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, mocker):
    pwd_service = get_password_service()
    user = UserFactory(
        id=1,
        email="test@example.com",
        hashed_password=pwd_service.hash("secret"),
    )

    mock_repo = mocker.MagicMock()
    mock_repo.get_by_email = mocker.AsyncMock(return_value=user)

    mocker.patch(
        "app.api.v1.endpoints.auth.get_user_repository", return_value=mock_repo
    )
    mocker.patch("app.api.v1.endpoints.auth.pwd_service.verify", return_value=True)

    response = await client.post(
        "/api/v1/auth/login", json={"email": "test@example.com", "password": "secret"}
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data
    assert "expires_at" in data


@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient, mocker):
    # === Мокаем verify_token ===
    mocker.patch(
        "app.api.v1.endpoints.auth.verify_token",
        return_value={"sub": "1", "type": "refresh"},
    )

    # === Мокаем create_access_token и create_refresh_token ===
    mocker.patch(
        "app.api.v1.endpoints.auth.create_access_token", return_value="new-access-token"
    )
    mocker.patch(
        "app.api.v1.endpoints.auth.create_refresh_token",
        return_value="new-refresh-token",
    )

    # === Мокаем expires_at (через TokenOut) ===
    fake_expires_at = "2025-11-06T12:47:00Z"
    mocker.patch(
        "app.api.v1.endpoints.auth.TokenOut",
        return_value={
            "access_token": "new-access-token",
            "refresh_token": "new-refresh-token",
            "token_type": "bearer",
            "expires_at": fake_expires_at,
        },
    )

    # === Запрос ===
    response = await client.post(
        "/api/v1/auth/refresh", params={"refresh_token": "any-fake-token"}
    )

    # === Проверки ===
    assert response.status_code == 200
    data = response.json()

    assert data == {
        "access_token": "new-access-token",
        "refresh_token": "new-refresh-token",
        "token_type": "bearer",
        "expires_at": "2025-11-06T12:47:00+00:00Z",
    }

    # === Проверка вызовов ===
    from app.api.v1.endpoints.auth import (create_access_token,
                                           create_refresh_token)

    create_access_token.assert_called_once_with({"sub": "1"})
    create_refresh_token.assert_called_once_with({"sub": "1"})
