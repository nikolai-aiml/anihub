from pydantic import BaseModel


class StatisticsSummary(BaseModel):
    average_rating: float = 0.0
    total_ratings: int = 0
    library_total: int = 0
    favorites_total: int = 0
    reviews_total: int = 0


class GenreCount(BaseModel):
    genre: str
    count: int


class MonthActivity(BaseModel):
    month: str          # "2026-04"
    count: int


class UserStatistics(BaseModel):
    summary: StatisticsSummary
    ratings_distribution: dict[str, int]    # {"1": 0, "2": 0, ..., "10": 12}
    top_genres: list[GenreCount]
    activity_by_month: list[MonthActivity]