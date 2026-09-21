from fastapi import APIRouter
from app.schemas.profile import ProfileRead
from app.api.deps import CurrentUser, DbSession
from app.schemas.user import UserRead, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser) -> UserRead:
    return current_user

@router.get("/me/profile", response_model=ProfileRead)
async def get_my_profile(
    current_user: CurrentUser,
    db: DbSession,
) -> ProfileRead:
    """Профиль со статистикой (для dashboard)."""
    return await UserService(db).get_full_profile(current_user)

@router.patch("/me", response_model=UserRead)
async def update_me(
    data: UserUpdate,
    current_user: CurrentUser,
    db: DbSession,
) -> UserRead:
    return await UserService(db).update_profile(current_user, data)