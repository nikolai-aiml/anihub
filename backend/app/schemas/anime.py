from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.anime import AnimeStatus, AnimeType
from app.schemas.genre import GenreRead


class AnimeListItem(BaseModel):
    """Краткая информация для каталога (сетка карточек)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    title_en: str | None = None
    poster_url: str | None = None
    year: int | None = None
    type: AnimeType
    status: AnimeStatus
    episodes_total: int | None = None
    rating: float
    rating_count: int
    genres: list[GenreRead] = []


class AnimeRead(BaseModel):
    """Полная информация для страницы аниме."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    title_en: str | None = None
    title_jp: str | None = None
    alternative_titles: str | None = None
    description: str | None = None
    poster_url: str | None = None
    year: int | None = None
    type: AnimeType
    status: AnimeStatus
    episodes_total: int | None = None
    duration_minutes: int | None = None
    studio: str | None = None
    rating: float
    rating_count: int
    genres: list[GenreRead] = []
    created_at: datetime
    updated_at: datetime


class PaginatedAnime(BaseModel):
    """Ответ каталога с пагинацией."""

    items: list[AnimeListItem]
    total: int
    page: int
    size: int
    pages: int