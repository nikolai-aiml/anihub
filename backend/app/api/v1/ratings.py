from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DbSession, OptionalUser
from app.schemas.rating import RatingCreate, RatingRead, RatingSummary
from app.services.rating import RatingService

router = APIRouter(prefix="/anime/{anime_id}/rating", tags=["ratings"])


@router.get("", response_model=RatingSummary)
async def get_anime_rating(
    anime_id: int,
    db: DbSession,
    current_user: OptionalUser,
) -> RatingSummary:
    """Сводка: средний рейтинг, количество оценок, личная оценка (если авторизован)."""
    user_id = current_user.id if current_user else None
    return await RatingService(db).get_summary(anime_id, user_id)


@router.post("", response_model=RatingRead)
async def rate_anime(
    anime_id: int,
    data: RatingCreate,
    current_user: CurrentUser,
    db: DbSession,
) -> RatingRead:
    """Поставить или обновить оценку (1–10)."""
    return await RatingService(db).rate(current_user.id, anime_id, data.value)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def remove_rating(
    anime_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    """Удалить свою оценку."""
    await RatingService(db).remove_rating(current_user.id, anime_id)
    return None
