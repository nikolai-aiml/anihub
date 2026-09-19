from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.user import UserRead, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser) -> UserRead:
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_me(
    data: UserUpdate,
    current_user: CurrentUser,
    db: DbSession,
) -> UserRead:
    return await UserService(db).update_profile(current_user, data)