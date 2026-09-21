from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.achievement import Achievement, UserAchievement


class AchievementRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Achievement]:
        result = await self.db.execute(select(Achievement).order_by(Achievement.id))
        return list(result.scalars().all())

    async def get_by_code(self, code: str) -> Achievement | None:
        result = await self.db.execute(
            select(Achievement).where(Achievement.code == code)
        )
        return result.scalar_one_or_none()

    async def get_user_unlocked_ids(self, user_id: int) -> set[int]:
        result = await self.db.execute(
            select(UserAchievement.achievement_id).where(
                UserAchievement.user_id == user_id
            )
        )
        return {row[0] for row in result.all()}

    async def get_user_achievements(
        self, user_id: int
    ) -> list[UserAchievement]:
        result = await self.db.execute(
            select(UserAchievement)
            .where(UserAchievement.user_id == user_id)
            .options(selectinload(UserAchievement.achievement))
        )
        return list(result.scalars().all())

    async def unlock(self, user_id: int, achievement_id: int) -> UserAchievement:
        ua = UserAchievement(user_id=user_id, achievement_id=achievement_id)
        self.db.add(ua)
        await self.db.commit()

        result = await self.db.execute(
            select(UserAchievement)
            .where(UserAchievement.id == ua.id)
            .options(selectinload(UserAchievement.achievement))
        )
        return result.scalar_one()