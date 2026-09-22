from datetime import datetime, timedelta

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.anime import Anime, anime_genres
from app.models.favorite import Favorite
from app.models.genre import Genre
from app.models.library import LibraryEntry
from app.models.rating import Rating


class RecommendationsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_continue_watching(self, user_id: int, limit: int = 10) -> list[Anime]:
        """Недавно добавленные в библиотеку."""
        result = await self.db.execute(
            select(Anime)
            .join(LibraryEntry, LibraryEntry.anime_id == Anime.id)
            .where(LibraryEntry.user_id == user_id)
            .options(selectinload(Anime.genres))
            .order_by(LibraryEntry.updated_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_top_user_genres(self, user_id: int, limit: int = 3) -> list[str]:
        """Топ жанров пользователя (по библиотеке + избранному + оценкам)."""
        # Собираем anime_ids пользователя
        library_result = await self.db.execute(
            select(LibraryEntry.anime_id).where(LibraryEntry.user_id == user_id)
        )
        fav_result = await self.db.execute(
            select(Favorite.anime_id).where(Favorite.user_id == user_id)
        )
        rating_result = await self.db.execute(
            select(Rating.anime_id).where(Rating.user_id == user_id)
        )

        anime_ids = set()
        for row in library_result.all():
            anime_ids.add(row[0])
        for row in fav_result.all():
            anime_ids.add(row[0])
        for row in rating_result.all():
            anime_ids.add(row[0])

        if not anime_ids:
            return []

        # Считаем жанры
        result = await self.db.execute(
            select(Genre.slug, func.count(anime_genres.c.anime_id).label("count"))
            .join(anime_genres, Genre.id == anime_genres.c.genre_id)
            .where(anime_genres.c.anime_id.in_(anime_ids))
            .group_by(Genre.slug)
            .order_by(desc("count"))
            .limit(limit)
        )
        return [row[0] for row in result.all()]

    async def get_recommendations(
        self,
        user_id: int,
        genre_slugs: list[str],
        limit: int = 10,
    ) -> list[Anime]:
        """Аниме по любимым жанрам, которых НЕТ у пользователя."""
        if not genre_slugs:
            # Если нет жанров — вернём популярное
            return await self.get_popular(limit)

        # Anime_ids пользователя (чтобы исключить)
        library_result = await self.db.execute(
            select(LibraryEntry.anime_id).where(LibraryEntry.user_id == user_id)
        )
        fav_result = await self.db.execute(
            select(Favorite.anime_id).where(Favorite.user_id == user_id)
        )

        user_anime_ids = set()
        for row in library_result.all():
            user_anime_ids.add(row[0])
        for row in fav_result.all():
            user_anime_ids.add(row[0])

        # Ищем аниме с этими жанрами, которых нет у пользователя
        stmt = (
            select(Anime)
            .join(anime_genres, Anime.id == anime_genres.c.anime_id)
            .join(Genre, Genre.id == anime_genres.c.genre_id)
            .where(Genre.slug.in_(genre_slugs))
            .options(selectinload(Anime.genres))
            .group_by(Anime.id)
            .order_by(desc(Anime.rating))
            .limit(limit * 2)   # берём с запасом, потом отфильтруем
        )

        result = await self.db.execute(stmt)
        candidates = list(result.scalars().all())

        # Фильтруем тех, кого нет у пользователя
        filtered = [a for a in candidates if a.id not in user_anime_ids]
        return filtered[:limit]

    async def get_popular(self, limit: int = 10) -> list[Anime]:
        """Топ по рейтингу."""
        result = await self.db.execute(
            select(Anime)
            .options(selectinload(Anime.genres))
            .where(Anime.rating_count > 0)
            .order_by(desc(Anime.rating), desc(Anime.rating_count))
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_new_releases(self, limit: int = 10) -> list[Anime]:
        """Аниме последних лет."""
        current_year = datetime.now().year
        result = await self.db.execute(
            select(Anime)
            .options(selectinload(Anime.genres))
            .where(Anime.year >= current_year - 3)
            .order_by(desc(Anime.year), desc(Anime.rating))
            .limit(limit)
        )
        return list(result.scalars().all())