from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)

    async def get_profile(self, user: User) -> User:
        return user

    async def update_profile(self, user: User, data: UserUpdate) -> User:
        # exclude_unset=True — берём только те поля, что реально переданы
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            return user

        # Проверяем уникальность username, если он меняется
        if "username" in update_data and update_data["username"] != user.username:
            existing = await self.users.get_by_username(update_data["username"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username уже занят",
                )

        # Проверяем уникальность email, если он меняется
        if "email" in update_data and update_data["email"] != user.email:
            existing = await self.users.get_by_email(update_data["email"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email уже зарегистрирован",
                )

        return await self.users.update(user, update_data)
