from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.recommendations import RecommendationsRepository
from app.schemas.anime import AnimeListItem
from app.schemas.recommendations import UserDashboard


class RecommendationsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = RecommendationsRepository(db)

    async def get_dashboard(self, user_id: int) -> UserDashboard:
        # Топ жанры
        top_genres = await self.repo.get_top_user_genres(user_id, limit=3)

        # Все секции
        continue_watching = await self.repo.get_continue_watching(user_id, limit=10)
        recommendations = await self.repo.get_recommendations(
            user_id, top_genres, limit=10
        )
        popular = await self.repo.get_popular(limit=10)
        new_releases = await self.repo.get_new_releases(limit=10)

        def convert(items):
            return [
                AnimeListItem.model_validate(a)
                for a in items
            ]

        return UserDashboard(
            continue_watching=convert(continue_watching),
            recommendations=convert(recommendations),
            popular=convert(popular),
            new_releases=convert(new_releases),
            top_genres=top_genres,
        )