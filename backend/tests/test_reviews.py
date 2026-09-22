"""Тесты отзывов и лайков."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_review(client: AsyncClient, user_headers, anime):
    """Создать отзыв."""
    response = await client.post(
        f"/api/v1/anime/{anime.id}/reviews",
        headers=user_headers,
        json={"text": "Отличное аниме, рекомендую!", "rating": 9},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Отличное аниме, рекомендую!"
    assert data["rating"] == 9
    assert data["is_own"] is True


@pytest.mark.asyncio
async def test_create_review_short_text(client: AsyncClient, user_headers, anime):
    """Короткий текст → 422."""
    response = await client.post(
        f"/api/v1/anime/{anime.id}/reviews",
        headers=user_headers,
        json={"text": "ok"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_review_duplicate(client: AsyncClient, user_headers, anime):
    """Второй отзыв от того же user → 409."""
    await client.post(
        f"/api/v1/anime/{anime.id}/reviews",
        headers=user_headers,
        json={"text": "Первый отзыв на это аниме"},
    )
    response = await client.post(
        f"/api/v1/anime/{anime.id}/reviews",
        headers=user_headers,
        json={"text": "Второй отзыв на это аниме"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_own_review(client: AsyncClient, user_headers, anime):
    """Обновить свой отзыв."""
    r = await client.post(
        f"/api/v1/anime/{anime.id}/reviews",
        headers=user_headers,
        json={"text": "Исходный текст отзыва"},
    )
    review_id = r.json()["id"]

    response = await client.patch(
        f"/api/v1/reviews/{review_id}",
        headers=user_headers,
        json={"text": "Обновлённый текст отзыва"},
    )
    assert response.status_code == 200
    assert response.json()["text"] == "Обновлённый текст отзыва"


@pytest.mark.asyncio
async def test_update_other_user_review(
    client: AsyncClient, user_headers, user2_headers, anime
):
    """Обновить чужой отзыв → 403."""
    r = await client.post(
        f"/api/v1/anime/{anime.id}/reviews",
        headers=user_headers,
        json={"text": "Мой отзыв на аниме"},
    )
    review_id = r.json()["id"]

    response = await client.patch(
        f"/api/v1/reviews/{review_id}",
        headers=user2_headers,
        json={"text": "Попытка взлома"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_other_user_review(
    client: AsyncClient, user_headers, user2_headers, anime
):
    """Удалить чужой отзыв → 403."""
    r = await client.post(
        f"/api/v1/anime/{anime.id}/reviews",
        headers=user_headers,
        json={"text": "Мой отзыв на аниме"},
    )
    review_id = r.json()["id"]

    response = await client.delete(
        f"/api/v1/reviews/{review_id}",
        headers=user2_headers,
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_like_review(
    client: AsyncClient, user_headers, user2_headers, anime
):
    """Лайкнуть чужой отзыв."""
    r = await client.post(
        f"/api/v1/anime/{anime.id}/reviews",
        headers=user_headers,
        json={"text": "Мой отзыв для лайка"},
    )
    review_id = r.json()["id"]

    response = await client.post(
        f"/api/v1/reviews/{review_id}/like",
        headers=user2_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_liked"] is True
    assert data["likes_count"] == 1


@pytest.mark.asyncio
async def test_cannot_like_own_review(client: AsyncClient, user_headers, anime):
    """Нельзя лайкать свой отзыв → 400."""
    r = await client.post(
        f"/api/v1/anime/{anime.id}/reviews",
        headers=user_headers,
        json={"text": "Свой отзыв для теста"},
    )
    review_id = r.json()["id"]

    response = await client.post(
        f"/api/v1/reviews/{review_id}/like",
        headers=user_headers,
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_unlike_review(
    client: AsyncClient, user_headers, user2_headers, anime
):
    """Убрать лайк."""
    r = await client.post(
        f"/api/v1/anime/{anime.id}/reviews",
        headers=user_headers,
        json={"text": "Отзыв для анлайка"},
    )
    review_id = r.json()["id"]

    await client.post(
        f"/api/v1/reviews/{review_id}/like",
        headers=user2_headers,
    )
    response = await client.delete(
        f"/api/v1/reviews/{review_id}/like",
        headers=user2_headers,
    )
    assert response.status_code == 200
    assert response.json()["is_liked"] is False
    assert response.json()["likes_count"] == 0


@pytest.mark.asyncio
async def test_double_like(client: AsyncClient, user_headers, user2_headers, anime):
    """Два лайка от одного user → 409."""
    r = await client.post(
        f"/api/v1/anime/{anime.id}/reviews",
        headers=user_headers,
        json={"text": "Отзыв для двойного лайка"},
    )
    review_id = r.json()["id"]

    await client.post(
        f"/api/v1/reviews/{review_id}/like",
        headers=user2_headers,
    )
    response = await client.post(
        f"/api/v1/reviews/{review_id}/like",
        headers=user2_headers,
    )
    assert response.status_code == 409