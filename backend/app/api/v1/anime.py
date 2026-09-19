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


@router.get("/{anime_id}", response_model=AnimeRead)
async def get_anime(anime_id: int, db: DbSession) -> AnimeRead:
    return await AnimeService(db).get_anime(anime_id)