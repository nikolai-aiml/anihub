from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username_or_email(self, value: str) -> User | None:
        result = await self.db.execute(
            select(User).where(or_(User.username == value, User.email == value))
        )
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user: User, data: dict) -> User:
        for field, value in data.items():
            setattr(user, field, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_profile_stats(self, user_id: int) -> dict[str, int]:
        """Считает статистику пользователя для профиля."""
        from app.models.favorite import Favorite
        from app.models.library import LibraryEntry
        from app.models.rating import Rating
        from app.models.review import Review

        async def _count(model, **filters):
            stmt = select(func.count()).select_from(model)
            for key, value in filters.items():
                stmt = stmt.where(getattr(model, key) == value)
            result = await self.db.execute(stmt)
            return result.scalar_one()

        return {
            "library_total": await _count(LibraryEntry, user_id=user_id),
            "ratings_total": await _count(Rating, user_id=user_id),
            "reviews_total": await _count(Review, user_id=user_id),
            "favorites_total": await _count(Favorite, user_id=user_id),
        }