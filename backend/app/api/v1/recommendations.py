from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.recommendations import UserDashboard
from app.services.recommendations import RecommendationsService

router = APIRouter(prefix="/users/me/dashboard", tags=["recommendations"])


@router.get("", response_model=UserDashboard)
async def get_dashboard(
    current_user: CurrentUser,
    db: DbSession,
) -> UserDashboard:
    """Персональный dashboard: рекомендации, продолжить, популярное, новинки."""
    return await RecommendationsService(db).get_dashboard(current_user.id)