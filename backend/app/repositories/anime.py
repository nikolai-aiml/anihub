from sqlalchemy import Select, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.anime import Anime, AnimeStatus, AnimeType
from app.models.genre import Genre


class AnimeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, anime_id: int) -> Anime | None:
        result = await self.db.execute(
            select(Anime).where(Anime.id == anime_id).options(selectinload(Anime.genres))
        )
        return result.scalar_one_or_none()

    def _build_query(
        self,
        search: str | None = None,
        genre_slug: str | None = None,
        year: int | None = None,
        anime_type: AnimeType | None = None,
        status: AnimeStatus | None = None,
        studio: str | None = None,
    ) -> Select:
        stmt = select(Anime).options(selectinload(Anime.genres))

        if search:
            pattern = f"%{search.lower()}%"
            stmt = stmt.where(
                or_(
                    func.lower(Anime.title).like(pattern),
                    func.lower(Anime.title_en).like(pattern),
                    func.lower(Anime.title_jp).like(pattern),
                    func.lower(Anime.alternative_titles).like(pattern),
                )
            )

        if genre_slug:
            stmt = stmt.join(Anime.genres).where(Genre.slug == genre_slug)

        if year:
            stmt = stmt.where(Anime.year == year)

        if anime_type:
            stmt = stmt.where(Anime.type == anime_type)

        if status:
            stmt = stmt.where(Anime.status == status)

        if studio:
            stmt = stmt.where(func.lower(Anime.studio) == studio.lower())

        return stmt

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
    ) -> tuple[list[Anime], int]:
        stmt = self._build_query(
            search=search,
            genre_slug=genre_slug,
            year=year,
            anime_type=anime_type,
            status=status,
            studio=studio,
        )

        # Сортировка
        sort_column = {
            "rating": Anime.rating,
            "year": Anime.year,
            "title": Anime.title,
            "created_at": Anime.created_at,
        }.get(sort, Anime.rating)

        if order == "asc":
            stmt = stmt.order_by(sort_column.asc())
        else:
            stmt = stmt.order_by(sort_column.desc())

        # Считаем общее количество (без limit/offset)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar_one()

        # Пагинация
        offset = (page - 1) * size
        stmt = stmt.offset(offset).limit(size)

        result = await self.db.execute(stmt)
        items = result.scalars().all()

        return list(items), total