from fastapi import APIRouter

from app.api.deps import DbSession
from app.schemas.episode import EpisodeRead
from app.services.episode import EpisodeService

router = APIRouter(prefix="/anime/{anime_id}/episodes", tags=["episodes"])


@router.get("", response_model=list[EpisodeRead])
async def list_episodes(
    anime_id: int,
    db: DbSession,
) -> list[EpisodeRead]:
    """Список эпизодов аниме."""
    return await EpisodeService(db).list_episodes(anime_id)


@router.get("/{number}", response_model=EpisodeRead)
async def get_episode(
    anime_id: int,
    number: int,
    db: DbSession,
) -> EpisodeRead:
    """Конкретный эпизод."""
    return await EpisodeService(db).get_episode(anime_id, number)