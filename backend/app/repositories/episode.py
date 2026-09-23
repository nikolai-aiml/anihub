from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.episode import Episode


class EpisodeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_anime(self, anime_id: int) -> list[Episode]:
        result = await self.db.execute(
            select(Episode)
            .where(Episode.anime_id == anime_id)
            .order_by(Episode.number)
        )
        return list(result.scalars().all())

    async def get_by_anime_and_number(
        self, anime_id: int, number: int
    ) -> Episode | None:
        result = await self.db.execute(
            select(Episode).where(
                Episode.anime_id == anime_id,
                Episode.number == number,
            )
        )
        return result.scalar_one_or_none()