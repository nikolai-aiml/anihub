from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.anime import Anime, anime_genres
from app.models.favorite import Favorite
from app.models.genre import Genre
from app.models.library import LibraryEntry
from app.models.rating import Rating
from app.models.review import Review


class StatisticsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_summary(self, user_id: int) -> dict:
        # Средняя оценка и количество
        rating_result = await self.db.execute(
            select(
                func.avg(Rating.value).label("avg"),
                func.count(Rating.id).label("count"),
            ).where(Rating.user_id == user_id)
        )
        rating_row = rating_result.one()
        avg = round(float(rating_row.avg), 2) if rating_row.avg is not None else 0.0
        total_ratings = int(rating_row.count)

        # Библиотека
        library_result = await self.db.execute(
            select(func.count(LibraryEntry.id)).where(LibraryEntry.user_id == user_id)
        )
        library_total = library_result.scalar_one()

        # Избранное
        fav_result = await self.db.execute(
            select(func.count(Favorite.id)).where(Favorite.user_id == user_id)
        )
        favorites_total = fav_result.scalar_one()

        # Отзывы
        review_result = await self.db.execute(
            select(func.count(Review.id)).where(Review.user_id == user_id)
        )
        reviews_total = review_result.scalar_one()

        return {
            "average_rating": avg,
            "total_ratings": total_ratings,
            "library_total": library_total,
            "favorites_total": favorites_total,
            "reviews_total": reviews_total,
        }

    async def get_ratings_distribution(self, user_id: int) -> dict[str, int]:
        result = await self.db.execute(
            select(Rating.value, func.count(Rating.id))
            .where(Rating.user_id == user_id)
            .group_by(Rating.value)
        )
        counts = {int(row[0]): int(row[1]) for row in result.all()}
        # Возвращаем все значения 1–10
        return {str(i): counts.get(i, 0) for i in range(1, 11)}

    async def get_top_genres(self, user_id: int, limit: int = 5) -> list[dict]:
        """Топ жанров по библиотеке и избранному пользователя."""
        # Собираем anime_id из библиотеки + избранного + оценок (уникальные)
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
            select(Genre.name, func.count(anime_genres.c.anime_id).label("count"))
            .join(anime_genres, Genre.id == anime_genres.c.genre_id)
            .where(anime_genres.c.anime_id.in_(anime_ids))
            .group_by(Genre.name)
            .order_by(func.count(anime_genres.c.anime_id).desc())
            .limit(limit)
        )
        return [{"genre": row[0], "count": int(row[1])} for row in result.all()]

    async def get_activity_by_month(self, user_id: int, months: int = 6) -> list[dict]:
        """Активность за последние N месяцев (по датам оценок)."""
        result = await self.db.execute(
            select(
                func.to_char(Rating.created_at, "YYYY-MM").label("month"),
                func.count(Rating.id).label("count"),
            )
            .where(Rating.user_id == user_id)
            .group_by("month")
            .order_by("month")
        )
        rows = result.all()

        # Возвращаем последние N месяцев
        data = [{"month": row[0], "count": int(row[1])} for row in rows]
        return data[-months:] if len(data) > months else data