from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.favorite import Favorite
from app.models.library import LibraryEntry
from app.models.rating import Rating
from app.models.review import Review
from app.models.user import User
from app.repositories.achievement import AchievementRepository
from app.schemas.achievement import UserAchievementRead


class AchievementService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.achievements = AchievementRepository(db)

    async def _count(self, model, user_id: int) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(model).where(model.user_id == user_id)
        )
        return result.scalar_one()

    async def _get_progress_map(self, user_id: int) -> dict[str, int]:
        """Считает текущий прогресс по всем категориям."""
        library_count = await self._count(LibraryEntry, user_id)
        ratings_count = await self._count(Rating, user_id)
        reviews_count = await self._count(Review, user_id)
        favorites_count = await self._count(Favorite, user_id)

        # Возраст аккаунта в днях
        user_result = await self.db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one()
        from datetime import datetime, timezone

        age_days = (datetime.now(timezone.utc) - user.created_at).days

        return {
            "library": library_count,
            "ratings": ratings_count,
            "reviews": reviews_count,
            "favorites": favorites_count,
            "account_age_days": age_days,
        }

    async def get_user_achievements(
        self, user_id: int
    ) -> list[UserAchievementRead]:
        all_achievements = await self.achievements.get_all()
        unlocked_map = {
            ua.achievement_id: ua.unlocked_at
            for ua in await self.achievements.get_user_achievements(user_id)
        }

        progress_map = await self._get_progress_map(user_id)

        result = []
        for ach in all_achievements:
            # Прогресс в зависимости от категории
            category_value = ach.category.value
            if category_value == "special":
                if ach.code == "veteran_30":
                    current = progress_map["account_age_days"]
                elif ach.code == "all_rounder":
                    # минимум из 4 категорий
                    current = min(
                        progress_map["library"],
                        progress_map["ratings"],
                        progress_map["reviews"],
                        progress_map["favorites"],
                    )
                else:
                    current = 0
            else:
                current = progress_map.get(category_value, 0)

            is_unlocked = ach.id in unlocked_map

            result.append(
                UserAchievementRead(
                    id=ach.id,
                    code=ach.code,
                    title=ach.title,
                    description=ach.description,
                    icon=ach.icon,
                    rarity=ach.rarity,
                    category=ach.category,
                    target=ach.target,
                    progress=min(current, ach.target) if not is_unlocked else ach.target,
                    is_unlocked=is_unlocked,
                    unlocked_at=unlocked_map.get(ach.id),
                )
            )

        return result

    async def check_and_unlock(self, user_id: int) -> list[str]:
        """Проверяет и выдаёт новые достижения. Возвращает список кодов."""
        all_achievements = await self.achievements.get_all()
        unlocked_ids = await self.achievements.get_user_unlocked_ids(user_id)
        progress_map = await self._get_progress_map(user_id)

        newly_unlocked: list[str] = []

        for ach in all_achievements:
            if ach.id in unlocked_ids:
                continue

            category_value = ach.category.value

            if category_value == "special":
                if ach.code == "veteran_30":
                    current = progress_map["account_age_days"]
                elif ach.code == "all_rounder":
                    current = min(
                        progress_map["library"],
                        progress_map["ratings"],
                        progress_map["reviews"],
                        progress_map["favorites"],
                    )
                else:
                    current = 0
            else:
                current = progress_map.get(category_value, 0)

            if current >= ach.target:
                await self.achievements.unlock(user_id, ach.id)
                newly_unlocked.append(ach.code)

        return newly_unlocked