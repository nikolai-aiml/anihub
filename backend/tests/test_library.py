"""Тесты библиотеки."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_to_library(client: AsyncClient, user_headers, anime):
    """Добавить в библиотеку."""
    response = await client.post(
        f"/api/v1/users/me/library/{anime.id}",
        headers=user_headers,
        json={"status": "watching"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["anime_id"] == anime.id
    assert data["status"] == "watching"


@pytest.mark.asyncio
async def test_add_to_library_duplicate(client: AsyncClient, user_headers, anime):
    """Дубликат → 409."""
    await client.post(
        f"/api/v1/users/me/library/{anime.id}",
        headers=user_headers,
        json={"status": "watching"},
    )
    response = await client.post(
        f"/api/v1/users/me/library/{anime.id}",
        headers=user_headers,
        json={"status": "planned"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_library_status(client: AsyncClient, user_headers, anime):
    """Обновить статус."""
    await client.post(
        f"/api/v1/users/me/library/{anime.id}",
        headers=user_headers,
        json={"status": "watching"},
    )
    response = await client.patch(
        f"/api/v1/users/me/library/{anime.id}",
        headers=user_headers,
        json={"status": "completed"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_library_filter_by_status(client: AsyncClient, user_headers, anime, db_session):
    """Фильтр по статусу."""
    from tests.conftest import create_test_anime

    anime2 = await create_test_anime(db_session, title="Anime 2")

    await client.post(
        f"/api/v1/users/me/library/{anime.id}",
        headers=user_headers,
        json={"status": "watching"},
    )
    await client.post(
        f"/api/v1/users/me/library/{anime2.id}",
        headers=user_headers,
        json={"status": "completed"},
    )

    response = await client.get(
        "/api/v1/users/me/library?status=watching",
        headers=user_headers,
    )
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "watching"


@pytest.mark.asyncio
async def test_library_stats(client: AsyncClient, user_headers, anime):
    """Статистика по статусам."""
    await client.post(
        f"/api/v1/users/me/library/{anime.id}",
        headers=user_headers,
        json={"status": "watching"},
    )
    response = await client.get(
        "/api/v1/users/me/library/stats",
        headers=user_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["watching"] == 1
    assert data["completed"] == 0


@pytest.mark.asyncio
async def test_remove_from_library(client: AsyncClient, user_headers, anime):
    """Удалить из библиотеки."""
    await client.post(
        f"/api/v1/users/me/library/{anime.id}",
        headers=user_headers,
        json={"status": "watching"},
    )
    response = await client.delete(
        f"/api/v1/users/me/library/{anime.id}",
        headers=user_headers,
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_invalid_status(client: AsyncClient, user_headers, anime):
    """Невалидный статус → 422."""
    response = await client.post(
        f"/api/v1/users/me/library/{anime.id}",
        headers=user_headers,
        json={"status": "invalid_status"},
    )
    assert response.status_code == 422