from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.library import LibraryEntry, LibraryStatus
from app.repositories.anime import AnimeRepository
from app.repositories.library import LibraryRepository


class LibraryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.library = LibraryRepository(db)
        self.anime = AnimeRepository(db)

    async def list_library(
        self,
        user_id: int,
        status_filter: LibraryStatus | None = None,
    ) -> list[LibraryEntry]:
        return await self.library.get_list(user_id, status_filter)

    async def add_to_library(
        self,
        user_id: int,
        anime_id: int,
        entry_status: LibraryStatus = LibraryStatus.PLANNED,
    ) -> LibraryEntry:
        # Проверяем, что аниме существует
        anime = await self.anime.get_by_id(anime_id)
        if not anime:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Аниме не найдено",
            )

        # Проверяем, что не добавлено
        existing = await self.library.get_by_user_and_anime(user_id, anime_id)
        if existing:
            raise HTTPException(
                status_code=http_status.HTTP_409_CONFLICT,
                detail="Аниме уже в библиотеке",
            )

        return await self.library.add(user_id, anime_id, entry_status)

    async def update_status(
        self, user_id: int, anime_id: int, new_status: LibraryStatus
    ) -> LibraryEntry:
        entry = await self.library.get_by_user_and_anime(user_id, anime_id)
        if not entry:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Аниме не в библиотеке",
            )

        updated = await self.library.update_status(user_id, anime_id, new_status)
        if not updated:
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка обновления",
            )
        return updated

    async def remove_from_library(self, user_id: int, anime_id: int) -> None:
        entry = await self.library.get_by_user_and_anime(user_id, anime_id)
        if not entry:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Аниме не в библиотеке",
            )
        await self.library.remove(user_id, anime_id)

    async def get_status_counts(self, user_id: int) -> dict[str, int]:
        counts = await self.library.count_by_status(user_id)
        # Возвращаем все статусы, даже если 0
        return {
            s.value: counts.get(s.value, 0)
            for s in LibraryStatus
        }