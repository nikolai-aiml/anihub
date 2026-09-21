from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.anime import Anime
from app.models.favorite import Favorite


class FavoriteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self, user_id: int) -> list[Favorite]:
        result = await self.db.execute(
            select(Favorite)
            .where(Favorite.user_id == user_id)
            .options(selectinload(Favorite.anime).selectinload(Anime.genres))
            .order_by(Favorite.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_user_and_anime(
        self, user_id: int, anime_id: int
    ) -> Favorite | None:
        result = await self.db.execute(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.anime_id == anime_id,
            )
        )
        return result.scalar_one_or_none()

    async def add(self, user_id: int, anime_id: int) -> Favorite:
        favorite = Favorite(user_id=user_id, anime_id=anime_id)
        self.db.add(favorite)
        await self.db.commit()

        # Перезагружаем с eager-load anime + genres
        result = await self.db.execute(
            select(Favorite)
            .where(Favorite.id == favorite.id)
            .options(selectinload(Favorite.anime).selectinload(Anime.genres))
        )
        return result.scalar_one()

    async def remove(self, user_id: int, anime_id: int) -> None:
        """Удаляет из избранного напрямую через SQL DELETE."""
        await self.db.execute(
            delete(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.anime_id == anime_id,
            )
        )
        await self.db.commit()