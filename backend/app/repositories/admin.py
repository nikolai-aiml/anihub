from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.anime import Anime
from app.models.favorite import Favorite
from app.models.library import LibraryEntry
from app.models.rating import Rating
from app.models.review import Review
from app.models.user import User


class AdminRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_stats(self) -> dict:
        async def count(model, *where):
            stmt = select(func.count()).select_from(model)
            for w in where:
                stmt = stmt.where(w)
            result = await self.db.execute(stmt)
            return result.scalar_one()

        return {
            "users_total": await count(User),
            "users_active": await count(User, User.is_active == True),  # noqa
            "anime_total": await count(Anime),
            "reviews_total": await count(Review),
            "ratings_total": await count(Rating),
            "favorites_total": await count(Favorite),
            "library_total": await count(LibraryEntry),
        }

    async def list_users(self, limit: int = 100, offset: int = 0) -> list[User]:
        result = await self.db.execute(
            select(User).order_by(User.created_at.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def list_anime(self, limit: int = 100, offset: int = 0) -> list[Anime]:
        result = await self.db.execute(
            select(Anime).order_by(Anime.created_at.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def toggle_user_active(self, user: User) -> User:
        user.is_active = not user.is_active
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()

    async def delete_anime(self, anime: Anime) -> None:
        await self.db.delete(anime)
        await self.db.commit()