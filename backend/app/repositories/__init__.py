from app.repositories.achievement import AchievementRepository
from app.repositories.anime import AnimeRepository
from app.repositories.favorite import FavoriteRepository
from app.repositories.library import LibraryRepository
from app.repositories.notification import NotificationRepository
from app.repositories.rating import RatingRepository
from app.repositories.review import ReviewRepository
from app.repositories.statistics import StatisticsRepository
from app.repositories.user import UserRepository
from app.repositories.recommendations import RecommendationsRepository
from app.repositories.admin import AdminRepository
from app.repositories.episode import EpisodeRepository

__all__ = [
    "AchievementRepository",
    "EpisodeRepository",
    "AnimeRepository",
    "FavoriteRepository",
    "LibraryRepository",
    "RecommendationsRepository",
    "NotificationRepository",
    "RatingRepository",
    "ReviewRepository",
    "StatisticsRepository",
    "UserRepository",
    "AdminRepository",
]