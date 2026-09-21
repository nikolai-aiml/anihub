from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.anime import Anime
from app.models.library import LibraryEntry, LibraryStatus


class LibraryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        user_id: int,
        status: LibraryStatus | None = None,
    ) -> list[LibraryEntry]:
        stmt = (
            select(LibraryEntry)
            .where(LibraryEntry.user_id == user_id)
            .options(selectinload(LibraryEntry.anime).selectinload(Anime.genres))
            .order_by(LibraryEntry.updated_at.desc())
        )
        if status:
            stmt = stmt.where(LibraryEntry.status == status)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_user_and_anime(
        self, user_id: int, anime_id: int
    ) -> LibraryEntry | None:
        result = await self.db.execute(
            select(LibraryEntry).where(
                LibraryEntry.user_id == user_id,
                LibraryEntry.anime_id == anime_id,
            )
        )
        return result.scalar_one_or_none()

    async def add(
        self, user_id: int, anime_id: int, status: LibraryStatus
    ) -> LibraryEntry:
        entry = LibraryEntry(user_id=user_id, anime_id=anime_id, status=status)
        self.db.add(entry)
        await self.db.commit()

        # Перезагружаем с eager-load
        result = await self.db.execute(
            select(LibraryEntry)
            .where(LibraryEntry.id == entry.id)
            .options(selectinload(LibraryEntry.anime).selectinload(Anime.genres))
        )
        return result.scalar_one()

    async def update_status(
        self, user_id: int, anime_id: int, status: LibraryStatus
    ) -> LibraryEntry | None:
        entry = await self.get_by_user_and_anime(user_id, anime_id)
        if not entry:
            return None
        entry.status = status
        await self.db.commit()

        # Перезагружаем с eager-load
        result = await self.db.execute(
            select(LibraryEntry)
            .where(LibraryEntry.id == entry.id)
            .options(selectinload(LibraryEntry.anime).selectinload(Anime.genres))
        )
        return result.scalar_one()

    async def remove(self, user_id: int, anime_id: int) -> None:
        await self.db.execute(
            delete(LibraryEntry).where(
                LibraryEntry.user_id == user_id,
                LibraryEntry.anime_id == anime_id,
            )
        )
        await self.db.commit()

    async def count_by_status(self, user_id: int) -> dict[str, int]:
        """Считает количество записей по каждому статусу."""
        from sqlalchemy import func

        result = await self.db.execute(
            select(LibraryEntry.status, func.count(LibraryEntry.id))
            .where(LibraryEntry.user_id == user_id)
            .group_by(LibraryEntry.status)
        )
        return {status.value: count for status, count in result.all()}