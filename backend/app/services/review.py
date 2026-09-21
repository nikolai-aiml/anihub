from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review
from app.repositories.anime import AnimeRepository
from app.repositories.review import ReviewRepository
from app.schemas.review import ReviewRead


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.reviews = ReviewRepository(db)
        self.anime = AnimeRepository(db)

    async def _to_read(
        self, review: Review, user_id: int | None
    ) -> ReviewRead:
        """Преобразует Review в ReviewRead с флагами is_liked и is_own."""
        is_liked = False
        if user_id:
            like = await self.reviews.get_like(user_id, review.id)
            is_liked = like is not None

        return ReviewRead(
            id=review.id,
            anime_id=review.anime_id,
            rating=review.rating,
            text=review.text,
            likes_count=review.likes_count,
            created_at=review.created_at,
            updated_at=review.updated_at,
            user=review.user,
            is_liked=is_liked,
            is_own=(user_id == review.user_id) if user_id else False,
        )

    async def list_by_anime(
        self,
        anime_id: int,
        user_id: int | None = None,
        sort: str = "new",
        page: int = 1,
        size: int = 20,
    ) -> list[ReviewRead]:
        offset = (page - 1) * size
        reviews, _ = await self.reviews.list_by_anime(
            anime_id, sort=sort, limit=size, offset=offset
        )

        return [await self._to_read(r, user_id) for r in reviews]

    async def create(
        self,
        user_id: int,
        anime_id: int,
        text: str,
        rating: int | None,
    ) -> ReviewRead:
        anime = await self.anime.get_by_id(anime_id)
        if not anime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Аниме не найдено",
            )

        existing = await self.reviews.get_by_user_and_anime(user_id, anime_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Вы уже оставили отзыв на это аниме",
            )

        review = await self.reviews.create(user_id, anime_id, text, rating)
        return await self._to_read(review, user_id)

    async def update(
        self,
        user_id: int,
        review_id: int,
        text: str | None,
        rating: int | None,
    ) -> ReviewRead:
        review = await self.reviews.get_by_id(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Отзыв не найден",
            )
        if review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы можете редактировать только свои отзывы",
            )

        updated = await self.reviews.update(review, text, rating)
        return await self._to_read(updated, user_id)

    async def remove(self, user_id: int, review_id: int) -> None:
        review = await self.reviews.get_by_id(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Отзыв не найден",
            )
        if review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы можете удалять только свои отзывы",
            )
        await self.reviews.remove(review)

    async def like(self, user_id: int, review_id: int) -> dict:
        review = await self.reviews.get_by_id(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Отзыв не найден",
            )
        if review.user_id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Нельзя лайкать свой отзыв",
            )

        existing = await self.reviews.get_like(user_id, review_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Вы уже лайкнули этот отзыв",
            )

        await self.reviews.add_like(user_id, review_id)
        # Перезагружаем для получения актуального likes_count
        updated = await self.reviews.get_by_id(review_id)
        return {"is_liked": True, "likes_count": updated.likes_count}

    async def unlike(self, user_id: int, review_id: int) -> dict:
        review = await self.reviews.get_by_id(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Отзыв не найден",
            )

        existing = await self.reviews.get_like(user_id, review_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Лайк не найден",
            )

        await self.reviews.remove_like(user_id, review_id)
        updated = await self.reviews.get_by_id(review_id)
        return {"is_liked": False, "likes_count": updated.likes_count}