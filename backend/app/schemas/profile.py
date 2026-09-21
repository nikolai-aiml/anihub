from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProfileStats(BaseModel):
    """Счётчики для карточек профиля."""

    library_total: int = 0
    ratings_total: int = 0
    reviews_total: int = 0
    favorites_total: int = 0


class ProfileRead(BaseModel):
    """Полный профиль пользователя."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    avatar_url: str | None = None
    bio: str | None = None
    created_at: datetime
    stats: ProfileStats