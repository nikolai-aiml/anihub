"""Тесты оценок."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_rate_anime(client: AsyncClient, user_headers, anime):
    """Поставить оценку."""
    response = await client.post(
        f"/api/v1/anime/{anime.id}/rating",
        headers=user_headers,
        json={"value": 8},
    )
    assert response.status_code == 200
    assert response.json()["value"] == 8


@pytest.mark.asyncio
async def test_rate_anime_invalid_value(client: AsyncClient, user_headers, anime):
    """Оценка < 1 или > 10 → 422."""
    response = await client.post(
        f"/api/v1/anime/{anime.id}/rating",
        headers=user_headers,
        json={"value": 15},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_rate_upsert(client: AsyncClient, user_headers, anime):
    """Повторная оценка ОБНОВЛЯЕТ, а не создаёт вторую."""
    r1 = await client.post(
        f"/api/v1/anime/{anime.id}/rating",
        headers=user_headers,
        json={"value": 5},
    )
    rating_id = r1.json()["id"]

    r2 = await client.post(
        f"/api/v1/anime/{anime.id}/rating",
        headers=user_headers,
        json={"value": 10},
    )
    assert r2.status_code == 200
    assert r2.json()["id"] == rating_id   # тот же id
    assert r2.json()["value"] == 10


@pytest.mark.asyncio
async def test_rating_summary(client: AsyncClient, user_headers, anime):
    """Сводка по оценкам."""
    await client.post(
        f"/api/v1/anime/{anime.id}/rating",
        headers=user_headers,
        json={"value": 9},
    )
    response = await client.get(
        f"/api/v1/anime/{anime.id}/rating",
        headers=user_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_rating"] == 9
    assert "average" in data
    assert "count" in data


@pytest.mark.asyncio
async def test_rating_summary_guest(client: AsyncClient, anime):
    """Гость видит сводку без user_rating."""
    response = await client.get(f"/api/v1/anime/{anime.id}/rating")
    assert response.status_code == 200
    data = response.json()
    assert data["user_rating"] is None


@pytest.mark.asyncio
async def test_remove_rating(client: AsyncClient, user_headers, anime):
    """Удалить оценку."""
    await client.post(
        f"/api/v1/anime/{anime.id}/rating",
        headers=user_headers,
        json={"value": 7},
    )
    response = await client.delete(
        f"/api/v1/anime/{anime.id}/rating",
        headers=user_headers,
    )
    assert response.status_code == 204

    # Проверяем, что user_rating снова null
    r = await client.get(
        f"/api/v1/anime/{anime.id}/rating",
        headers=user_headers,
    )
    assert r.json()["user_rating"] is None