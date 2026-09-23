from fastapi import APIRouter, status

from app.api.deps import CurrentAdmin, DbSession
from app.schemas.admin import AdminAnimeRead, AdminStats, AdminUserRead
from app.services.admin import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStats)
async def get_stats(
    admin: CurrentAdmin,
    db: DbSession,
) -> AdminStats:
    return await AdminService(db).get_stats()


@router.get("/users", response_model=list[AdminUserRead])
async def list_users(
    admin: CurrentAdmin,
    db: DbSession,
) -> list[AdminUserRead]:
    return await AdminService(db).list_users()


@router.patch("/users/{user_id}/toggle-active", response_model=AdminUserRead)
async def toggle_user_active(
    user_id: int,
    admin: CurrentAdmin,
    db: DbSession,
) -> AdminUserRead:
    return await AdminService(db).toggle_user_active(user_id)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    admin: CurrentAdmin,
    db: DbSession,
) -> None:
    await AdminService(db).delete_user(user_id, admin.id)
    return None


@router.get("/anime", response_model=list[AdminAnimeRead])
async def list_anime(
    admin: CurrentAdmin,
    db: DbSession,
) -> list[AdminAnimeRead]:
    return await AdminService(db).list_anime()


@router.delete("/anime/{anime_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_anime(
    anime_id: int,
    admin: CurrentAdmin,
    db: DbSession,
) -> None:
    await AdminService(db).delete_anime(anime_id)
    return None