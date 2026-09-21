from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.achievement import AchievementCategory, AchievementRarity


class AchievementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    title: str
    description: str
    icon: str
    rarity: AchievementRarity
    category: AchievementCategory
    target: int


class UserAchievementRead(BaseModel):
    """Достижение с прогрессом пользователя."""

    id: int
    code: str
    title: str
    description: str
    icon: str
    rarity: AchievementRarity
    category: AchievementCategory
    target: int
    progress: int               # текущий прогресс
    is_unlocked: bool           # получено ли
    unlocked_at: datetime | None = None