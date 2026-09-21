from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rating import Rating
from app.repositories.anime import AnimeRepository
from app.repositories.rating import RatingRepository
from app.schemas.rating import RatingSummary


class RatingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ratings = RatingRepository(db)
        self.anime = AnimeRepository(db)

    async def get_summary(
        self, anime_id: int, user_id: int | None = None
    ) -> RatingSummary:
        """Сводка по оценкам: средний, количество, личная."""
        anime = await self.anime.get_by_id(anime_id)
        if not anime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Аниме не найдено",
            )

        user_rating = None
        if user_id:
            rating = await self.ratings.get_user_rating(user_id, anime_id)
            if rating:
                user_rating = rating.value

        return RatingSummary(
            average=anime.rating,
            count=anime.rating_count,
            user_rating=user_rating,
        )

    async def rate(
        self, user_id: int, anime_id: int, value: int
    ) -> Rating:
        anime = await self.anime.get_by_id(anime_id)
        if not anime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Аниме не найдено",
            )

        # Создаём или обновляем
        rating = await self.ratings.upsert(user_id, anime_id, value)

        # Пересчитываем средний рейтинг аниме
        await self.ratings.recalculate_anime_rating(anime_id)

        return rating

    async def remove_rating(self, user_id: int, anime_id: int) -> None:
        existing = await self.ratings.get_user_rating(user_id, anime_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Оценка не найдена",
            )
        await self.ratings.remove(user_id, anime_id)
        await self.ratings.recalculate_anime_rating(anime_id)