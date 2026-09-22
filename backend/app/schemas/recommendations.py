from pydantic import BaseModel

from app.schemas.anime import AnimeListItem


class UserDashboard(BaseModel):
    """Персональный dashboard для главной страницы."""

    continue_watching: list[AnimeListItem]   # недавно добавленные в библиотеку
    recommendations: list[AnimeListItem]     # рекомендации по жанрам
    popular: list[AnimeListItem]             # топ по рейтингу
    new_releases: list[AnimeListItem]        # последние годы
    top_genres: list[str]                    # топ-жанры пользователя