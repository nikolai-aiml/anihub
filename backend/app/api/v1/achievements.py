from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.achievement import UserAchievementRead
from app.services.achievement import AchievementService

router = APIRouter(prefix="/users/me/achievements", tags=["achievements"])


@router.get("", response_model=list[UserAchievementRead])
async def list_achievements(
    current_user: CurrentUser,
    db: DbSession,
) -> list[UserAchievementRead]:
    """Все достижения с прогрессом пользователя."""
    return await AchievementService(db).get_user_achievements(current_user.id)


@router.post("/check", response_model=list[str])
async def check_achievements(
    current_user: CurrentUser,
    db: DbSession,
) -> list[str]:
    """Проверить и выдать новые достижения. Возвращает коды новых."""
    return await AchievementService(db).check_and_unlock(current_user.id)