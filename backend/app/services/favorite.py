from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.favorite import Favorite
from app.repositories.anime import AnimeRepository
from app.repositories.favorite import FavoriteRepository


class FavoriteService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.favorites = FavoriteRepository(db)
        self.anime = AnimeRepository(db)

    async def list_favorites(self, user_id: int) -> list[Favorite]:
        return await self.favorites.get_list(user_id)

    async def add_to_favorites(self, user_id: int, anime_id: int) -> Favorite:
        # Проверяем, что аниме существует
        anime = await self.anime.get_by_id(anime_id)
        if not anime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Аниме не найдено",
            )

        # Проверяем, что не добавлено
        existing = await self.favorites.get_by_user_and_anime(user_id, anime_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Аниме уже в избранном",
            )

        return await self.favorites.add(user_id, anime_id)

    async def remove_from_favorites(self, user_id: int, anime_id: int) -> None:
        favorite = await self.favorites.get_by_user_and_anime(user_id, anime_id)
        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Аниме не в избранном",
            )
        await self.favorites.remove(favorite)