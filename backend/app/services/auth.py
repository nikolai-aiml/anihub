from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)

    async def register(self, data: UserCreate) -> User:
        if data.password != data.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароли не совпадают",
            )

        if await self.users.get_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username уже занят",
            )

        if await self.users.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email уже зарегистрирован",
            )

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
        )
        return await self.users.create(user)

    async def authenticate(self, login: str, password: str) -> User:
        user = await self.users.get_by_username_or_email(login)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт отключён",
            )
        return user