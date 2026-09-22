from app.services.achievement import AchievementService
from app.services.anime import AnimeService
from app.services.auth import AuthService
from app.services.favorite import FavoriteService
from app.services.library import LibraryService
from app.services.rating import RatingService
from app.services.review import ReviewService
from app.services.statistics import StatisticsService
from app.services.user import UserService
from app.services.notification import NotificationService
from app.services.recommendations import RecommendationsService

__all__ = [
    "AchievementService",
    "AnimeService",
    "AuthService",
    "FavoriteService",
    "LibraryService",
    "RatingService",
    "ReviewService",
    "StatisticsService",
    "UserService",
    "RecommendationsService",
    "NotificationService",
]