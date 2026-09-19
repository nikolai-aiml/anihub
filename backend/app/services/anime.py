from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.anime import Anime, AnimeStatus, AnimeType
from app.repositories.anime import AnimeRepository
from app.schemas.anime import AnimeRead, PaginatedAnime
from app.schemas.anime import AnimeListItem


class AnimeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.anime = AnimeRepository(db)

    async def get_anime(self, anime_id: int) -> Anime:
        anime = await self.anime.get_by_id(anime_id)
        if not anime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Аниме не найдено",
            )
        return anime

    async def list_anime(
        self,
        *,
        page: int = 1,
        size: int = 20,
        sort: str = "rating",
        order: str = "desc",
        search: str | None = None,
        genre_slug: str | None = None,
        year: int | None = None,
        anime_type: AnimeType | None = None,
        status: AnimeStatus | None = None,
        studio: str | None = None,
    ) -> PaginatedAnime:
        items, total = await self.anime.list_anime(
            page=page,
            size=size,
            sort=sort,
            order=order,
            search=search,
            genre_slug=genre_slug,
            year=year,
            anime_type=anime_type,
            status=status,
            studio=studio,
        )

        pages = (total + size - 1) // size if size > 0 else 1

        return PaginatedAnime(
            items=[AnimeListItem.model_validate(a) for a in items],
            total=total,
            page=page,
            size=size,
            pages=pages,
        )