from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.anime import Anime
from app.models.rating import Rating


class RatingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_rating(
        self, user_id: int, anime_id: int
    ) -> Rating | None:
        result = await self.db.execute(
            select(Rating).where(
                Rating.user_id == user_id,
                Rating.anime_id == anime_id,
            )
        )
        return result.scalar_one_or_none()

    async def upsert(
        self, user_id: int, anime_id: int, value: int
    ) -> Rating:
        """Создаёт или обновляет оценку."""
        existing = await self.get_user_rating(user_id, anime_id)
        if existing:
            existing.value = value
            await self.db.commit()
            await self.db.refresh(existing)
            return existing

        rating = Rating(user_id=user_id, anime_id=anime_id, value=value)
        self.db.add(rating)
        await self.db.commit()
        await self.db.refresh(rating)
        return rating

    async def remove(self, user_id: int, anime_id: int) -> None:
        await self.db.execute(
            delete(Rating).where(
                Rating.user_id == user_id,
                Rating.anime_id == anime_id,
            )
        )
        await self.db.commit()

    async def recalculate_anime_rating(self, anime_id: int) -> None:
        """Пересчитывает средний рейтинг и количество оценок аниме."""
        result = await self.db.execute(
            select(
                func.avg(Rating.value).label("avg"),
                func.count(Rating.id).label("count"),
            ).where(Rating.anime_id == anime_id)
        )
        row = result.one()
        avg = float(row.avg) if row.avg is not None else 0.0
        count = int(row.count)

        # Обновляем Anime
        anime_result = await self.db.execute(
            select(Anime).where(Anime.id == anime_id)
        )
        anime = anime_result.scalar_one()
        anime.rating = round(avg, 2)
        anime.rating_count = count
        await self.db.commit()