from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.anime import AnimeListItem


class FavoriteRead(BaseModel):
    """Избранное аниме с полной информацией для отображения."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    anime_id: int
    created_at: datetime
    anime: AnimeListItem


class FavoriteStatus(BaseModel):
    """Статус избранного для аниме (для кнопки ♡/♥)."""

    is_favorite: bool