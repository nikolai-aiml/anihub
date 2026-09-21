from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.statistics import UserStatistics
from app.services.statistics import StatisticsService

router = APIRouter(prefix="/users/me/statistics", tags=["statistics"])


@router.get("", response_model=UserStatistics)
async def get_statistics(
    current_user: CurrentUser,
    db: DbSession,
) -> UserStatistics:
    """Персональная статистика: рейтинги, жанры, активность."""
    return await StatisticsService(db).get_user_statistics(current_user.id)