from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.statistics import StatisticsRepository
from app.schemas.statistics import (
    GenreCount,
    MonthActivity,
    StatisticsSummary,
    UserStatistics,
)


class StatisticsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.stats = StatisticsRepository(db)

    async def get_user_statistics(self, user_id: int) -> UserStatistics:
        summary_data = await self.stats.get_summary(user_id)
        distribution = await self.stats.get_ratings_distribution(user_id)
        top_genres = await self.stats.get_top_genres(user_id, limit=5)
        activity = await self.stats.get_activity_by_month(user_id, months=6)

        return UserStatistics(
            summary=StatisticsSummary(**summary_data),
            ratings_distribution=distribution,
            top_genres=[GenreCount(**g) for g in top_genres],
            activity_by_month=[MonthActivity(**m) for m in activity],
        )