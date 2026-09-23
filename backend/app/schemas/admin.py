from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AdminStats(BaseModel):
    """Общая статистика для админки."""

    users_total: int
    users_active: int
    anime_total: int
    reviews_total: int
    ratings_total: int
    favorites_total: int
    library_total: int


class AdminUserRead(BaseModel):
    """Пользователь в админке."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime


class AdminAnimeRead(BaseModel):
    """Аниме в админке."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    title_en: str | None = None
    year: int | None = None
    rating: float
    rating_count: int
    created_at: datetime