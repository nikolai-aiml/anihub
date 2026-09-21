from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.favorite import FavoriteRead
from app.services.favorite import FavoriteService

router = APIRouter(prefix="/users/me/favorites", tags=["favorites"])


@router.get("", response_model=list[FavoriteRead])
async def list_favorites(
    current_user: CurrentUser,
    db: DbSession,
) -> list[FavoriteRead]:
    """Получить все избранные аниме текущего пользователя."""
    return await FavoriteService(db).list_favorites(current_user.id)


@router.post(
    "/{anime_id}",
    response_model=FavoriteRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_to_favorites(
    anime_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> FavoriteRead:
    """Добавить аниме в избранное."""
    return await FavoriteService(db).add_to_favorites(current_user.id, anime_id)


@router.delete("/{anime_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_favorites(
    anime_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    """Удалить аниме из избранного."""
    await FavoriteService(db).remove_from_favorites(current_user.id, anime_id)
    return None