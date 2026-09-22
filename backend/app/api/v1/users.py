from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.profile import ProfileRead
from app.schemas.user import PasswordChange, UserRead, UserUpdate
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

@router.post("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    data: PasswordChange,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    """Смена пароля текущего пользователя."""
    await UserService(db).change_password(
        current_user,
        data.old_password,
        data.new_password,
        data.new_password_confirm,
    )
    return None