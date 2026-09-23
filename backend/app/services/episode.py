from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.episode import Episode
from app.repositories.anime import AnimeRepository
from app.repositories.episode import EpisodeRepository


class EpisodeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.episodes = EpisodeRepository(db)
        self.anime = AnimeRepository(db)

    async def list_episodes(self, anime_id: int) -> list[Episode]:
        anime = await self.anime.get_by_id(anime_id)
        if not anime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Аниме не найдено",
            )
        return await self.episodes.list_by_anime(anime_id)

    async def get_episode(self, anime_id: int, number: int) -> Episode:
        episode = await self.episodes.get_by_anime_and_number(anime_id, number)
        if not episode:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Эпизод не найден",
            )
        return episode