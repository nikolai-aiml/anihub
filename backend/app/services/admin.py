from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.admin import AdminRepository
from app.schemas.admin import AdminStats


class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.admin = AdminRepository(db)

    async def get_stats(self) -> AdminStats:
        data = await self.admin.get_stats()
        return AdminStats(**data)

    async def list_users(self, limit: int = 100, offset: int = 0) -> list[User]:
        return await self.admin.list_users(limit, offset)

    async def list_anime(self, limit: int = 100, offset: int = 0):
        return await self.admin.list_anime(limit, offset)

    async def toggle_user_active(self, user_id: int) -> User:
        from app.repositories.user import UserRepository

        user = await UserRepository(self.db).get_by_id(user_id)
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        return await self.admin.toggle_user_active(user)

    async def delete_user(self, user_id: int, current_admin_id: int) -> None:
        from app.repositories.user import UserRepository

        if user_id == current_admin_id:
            raise HTTPException(400, "Нельзя удалить себя")

        user = await UserRepository(self.db).get_by_id(user_id)
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        await self.admin.delete_user(user)

    async def delete_anime(self, anime_id: int) -> None:
        from app.repositories.anime import AnimeRepository

        anime = await AnimeRepository(self.db).get_by_id(anime_id)
        if not anime:
            raise HTTPException(404, "Аниме не найдено")
        await self.admin.delete_anime(anime)