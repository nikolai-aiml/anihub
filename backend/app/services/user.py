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
    async def get_full_profile(self, user: User) -> "ProfileRead":
        """Возвращает профиль со статистикой."""
        from app.schemas.profile import ProfileRead, ProfileStats

        stats_dict = await self.users.get_profile_stats(user.id)

        return ProfileRead(
            id=user.id,
            username=user.username,
            email=user.email,
            avatar_url=user.avatar_url,
            bio=user.bio,
            created_at=user.created_at,
            stats=ProfileStats(**stats_dict),
        )

    async def change_password(
        self,
        user: User,
        old_password: str,
        new_password: str,
        new_password_confirm: str,
    ) -> None:
        from app.core.security import hash_password, verify_password

        # Проверка: старый пароль верный?
        if not verify_password(old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный текущий пароль",
            )

        # Проверка: новый == подтверждение?
        if new_password != new_password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Новые пароли не совпадают",
            )

        # Проверка: новый не равен старому?
        if verify_password(new_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Новый пароль не должен совпадать со старым",
            )

        # Меняем
        user.hashed_password = hash_password(new_password)
        await self.db.commit()

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
