from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.review import Review, ReviewLike


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, review_id: int) -> Review | None:
        result = await self.db.execute(
            select(Review)
            .where(Review.id == review_id)
            .options(selectinload(Review.user))
        )
        return result.scalar_one_or_none()

    async def get_by_user_and_anime(
        self, user_id: int, anime_id: int
    ) -> Review | None:
        result = await self.db.execute(
            select(Review)
            .where(
                Review.user_id == user_id,
                Review.anime_id == anime_id,
            )
            .options(selectinload(Review.user))
        )
        return result.scalar_one_or_none()

    async def list_by_anime(
        self,
        anime_id: int,
        sort: str = "new",
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Review], int]:
        stmt = (
            select(Review)
            .where(Review.anime_id == anime_id)
            .options(selectinload(Review.user))
        )

        if sort == "popular":
            stmt = stmt.order_by(Review.likes_count.desc(), Review.created_at.desc())
        else:
            stmt = stmt.order_by(Review.created_at.desc())

        # Всего
        count_stmt = select(func.count()).select_from(
            select(Review).where(Review.anime_id == anime_id).subquery()
        )
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar_one()

        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def create(
        self, user_id: int, anime_id: int, text: str, rating: int | None
    ) -> Review:
        review = Review(
            user_id=user_id,
            anime_id=anime_id,
            text=text,
            rating=rating,
        )
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review, ["user"])
        return review

    async def update(
        self, review: Review, text: str | None, rating: int | None
    ) -> Review:
        if text is not None:
            review.text = text
        if rating is not None:
            review.rating = rating
        await self.db.commit()
        await self.db.refresh(review, ["user"])
        return review

    async def remove(self, review: Review) -> None:
        await self.db.delete(review)
        await self.db.commit()

    # ============ ЛАЙКИ ============

    async def get_like(self, user_id: int, review_id: int) -> ReviewLike | None:
        result = await self.db.execute(
            select(ReviewLike).where(
                ReviewLike.user_id == user_id,
                ReviewLike.review_id == review_id,
            )
        )
        return result.scalar_one_or_none()

    async def add_like(self, user_id: int, review_id: int) -> None:
        like = ReviewLike(user_id=user_id, review_id=review_id)
        self.db.add(like)
        await self.db.commit()
        await self.recalculate_likes(review_id)

    async def remove_like(self, user_id: int, review_id: int) -> None:
        await self.db.execute(
            delete(ReviewLike).where(
                ReviewLike.user_id == user_id,
                ReviewLike.review_id == review_id,
            )
        )
        await self.db.commit()
        await self.recalculate_likes(review_id)

    async def recalculate_likes(self, review_id: int) -> None:
        result = await self.db.execute(
            select(func.count(ReviewLike.id)).where(ReviewLike.review_id == review_id)
        )
        count = result.scalar_one()
        await self.db.execute(
            update(Review).where(Review.id == review_id).values(likes_count=count)
        )
        await self.db.commit()

    async def get_liked_review_ids(
        self, user_id: int, review_ids: list[int]
    ) -> set[int]:
        """Возвращает ID отзывов, которые лайкнул user."""
        if not review_ids:
            return set()
        result = await self.db.execute(
            select(ReviewLike.review_id).where(
                ReviewLike.user_id == user_id,
                ReviewLike.review_id.in_(review_ids),
            )
        )
        return {row[0] for row in result.all()}