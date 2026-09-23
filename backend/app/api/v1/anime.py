from typing import Annotated

from fastapi import APIRouter, Query

from app.api.deps import DbSession
from app.models.anime import AnimeStatus, AnimeType
from app.schemas.anime import AnimeRead, PaginatedAnime
from app.services.anime import AnimeService

router = APIRouter(prefix="/anime", tags=["anime"])


@router.get("", response_model=PaginatedAnime)
async def list_anime(
    db: DbSession,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
    sort: Annotated[str, Query(pattern="^(rating|year|title|created_at)$")] = "rating",
    order: Annotated[str, Query(pattern="^(asc|desc)$")] = "desc",
    search: Annotated[str | None, Query(max_length=255)] = None,
    genre: Annotated[str | None, Query(max_length=50)] = None,
    year: Annotated[int | None, Query(ge=1900, le=2100)] = None,
    type: AnimeType | None = None,
    status: AnimeStatus | None = None,
    studio: Annotated[str | None, Query(max_length=150)] = None,
) -> PaginatedAnime:
    return await AnimeService(db).list_anime(
        page=page,
        size=size,
        sort=sort,
        order=order,
        search=search,
        genre_slug=genre,
        year=year,
        anime_type=type,
        status=status,
        studio=studio,
    )
@router.get("/spotlight")
async def get_spotlight(db: DbSession) -> dict:
    """Топ-5 месяца + Новинки сезона для главной страницы."""
    from datetime import datetime

    from sqlalchemy import desc, select
    from sqlalchemy.orm import selectinload

    from app.models.anime import Anime
    from app.schemas.anime import AnimeListItem

    # Топ-5 по рейтингу
    top_result = await db.execute(
        select(Anime)
        .options(selectinload(Anime.genres))
        .where(Anime.rating_count > 0)
        .order_by(desc(Anime.rating), desc(Anime.rating_count))
        .limit(5)
    )
    top_month = list(top_result.scalars().all())

    # Новинки — последние 2 года
    current_year = datetime.now().year

    new_result = await db.execute(
        select(Anime)
        .options(selectinload(Anime.genres))
        .where(Anime.year >= current_year - 2)
        .order_by(desc(Anime.year), desc(Anime.rating))
        .limit(5)
    )
    new_season = list(new_result.scalars().all())

    return {
        "top_month": [AnimeListItem.model_validate(a) for a in top_month],
        "new_season": [AnimeListItem.model_validate(a) for a in new_season],
    }

@router.get("/{anime_id}", response_model=AnimeRead)
async def get_anime(anime_id: int, db: DbSession) -> AnimeRead:
    return await AnimeService(db).get_anime(anime_id)