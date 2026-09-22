"""Тесты избранного."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_favorite(client: AsyncClient, user_headers, anime):
    """Добавить в избранное."""
    response = await client.post(
        f"/api/v1/users/me/favorites/{anime.id}",
        headers=user_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["anime_id"] == anime.id
    assert data["anime"]["id"] == anime.id


@pytest.mark.asyncio
async def test_add_favorite_unauthorized(client: AsyncClient, anime):
    """Без токена → 401."""
    response = await client.post(f"/api/v1/users/me/favorites/{anime.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_add_favorite_nonexistent_anime(client: AsyncClient, user_headers):
    """Несуществующее аниме → 404."""
    response = await client.post(
        "/api/v1/users/me/favorites/99999",
        headers=user_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_add_favorite_duplicate(client: AsyncClient, user_headers, anime):
    """Дубликат → 409."""
    await client.post(
        f"/api/v1/users/me/favorites/{anime.id}",
        headers=user_headers,
    )
    response = await client.post(
        f"/api/v1/users/me/favorites/{anime.id}",
        headers=user_headers,
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_list_favorites(client: AsyncClient, user_headers, anime):
    """Список избранного."""
    await client.post(
        f"/api/v1/users/me/favorites/{anime.id}",
        headers=user_headers,
    )
    response = await client.get(
        "/api/v1/users/me/favorites",
        headers=user_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["anime_id"] == anime.id


@pytest.mark.asyncio
async def test_remove_favorite(client: AsyncClient, user_headers, anime):
    """Удалить из избранного."""
    await client.post(
        f"/api/v1/users/me/favorites/{anime.id}",
        headers=user_headers,
    )
    response = await client.delete(
        f"/api/v1/users/me/favorites/{anime.id}",
        headers=user_headers,
    )
    assert response.status_code == 204

    # Проверяем, что список пуст
    response = await client.get(
        "/api/v1/users/me/favorites",
        headers=user_headers,
    )
    assert response.json() == []


@pytest.mark.asyncio
async def test_favorites_isolation(
    client: AsyncClient,
    user_headers,
    user2_headers,
    anime,
    db_session,
):
    """Пользователи видят ТОЛЬКО свои избранные."""
    # user добавляет
    await client.post(
        f"/api/v1/users/me/favorites/{anime.id}",
        headers=user_headers,
    )

    # user2 видит пусто
    response = await client.get(
        "/api/v1/users/me/favorites",
        headers=user2_headers,
    )
    assert response.json() == []