"""Тесты авторизации и регистрации."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """Успешная регистрация."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "hashed_password" not in data   # пароль НЕ возвращается
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_register_passwords_dont_match(client: AsyncClient):
    """Пароли не совпадают → 400."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "securepass123",
            "password_confirm": "different123",
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient, user):
    """Дубликат username → 409."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": user.username,   # уже существует
            "email": "another@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, user):
    """Дубликат email → 409."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "anotheruser",
            "email": user.email,   # уже существует
            "password": "securepass123",
            "password_confirm": "securepass123",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_short_password(client: AsyncClient):
    """Пароль < 8 → 422."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "short",
            "password_confirm": "short",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, user):
    """Успешный логин."""
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": user.username, "password": "test12345"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, user):
    """Неверный пароль → 401."""
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": user.username, "password": "wrongpass"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Несуществующий user → 401."""
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "nobody", "password": "test12345"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_authorized(client: AsyncClient, user_headers, user):
    """GET /users/me с токеном."""
    response = await client.get("/api/v1/users/me", headers=user_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user.username


@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    """GET /users/me без токена → 401."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_invalid_token(client: AsyncClient):
    """Невалидный токен → 401."""
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token_here"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_password_is_hashed(client: AsyncClient, db_session):
    """Проверяем, что пароль хешируется."""
    from sqlalchemy import select
    from app.models.user import User

    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "hashcheck",
            "email": "hash@example.com",
            "password": "plaintext123",
            "password_confirm": "plaintext123",
        },
    )

    result = await db_session.execute(
        select(User).where(User.username == "hashcheck")
    )
    user = result.scalar_one()
    assert user.hashed_password != "plaintext123"
    assert user.hashed_password.startswith("$argon2")   # Argon2