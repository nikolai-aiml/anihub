from app.schemas.anime import AnimeListItem, AnimeRead, PaginatedAnime
from app.schemas.favorite import FavoriteRead, FavoriteStatus
from app.schemas.genre import GenreRead
from app.schemas.library import (
    LibraryEntryCreate,
    LibraryEntryRead,
    LibraryEntryUpdate,
)
from app.schemas.notification import NotificationRead, UnreadCount
from app.schemas.recommendations import UserDashboard
from app.schemas.admin import AdminAnimeRead, AdminStats, AdminUserRead
from app.schemas.episode import EpisodeRead

from app.schemas.statistics import (
    GenreCount,
    MonthActivity,
    StatisticsSummary,
    UserStatistics,
)
from app.schemas.profile import ProfileRead, ProfileStats
from app.schemas.rating import RatingCreate, RatingRead, RatingSummary
from app.schemas.review import (
    ReviewAuthor,
    ReviewCreate,
    ReviewLikeStatus,
    ReviewRead,
    ReviewUpdate,
)
from app.schemas.achievement import AchievementRead, UserAchievementRead
from app.schemas.user import (
    PasswordChange,
    Token,
    TokenPayload,
    UserCreate,
    UserRead,
    UserUpdate,
)

__all__ = [
    "AdminAnimeRead",
    "EpisodeRead",
    "AdminStats",
    "AdminUserRead",
    "PasswordChange",
    "AnimeListItem",
    "AnimeRead",
    "FavoriteRead",
    "FavoriteStatus",
    "UserDashboard",
    "GenreRead",
    "LibraryEntryCreate",
    "LibraryEntryRead",
    "LibraryEntryUpdate",
    "PaginatedAnime",
    "ProfileRead",
    "ProfileStats",
    "RatingCreate",
    "RatingRead",
    "RatingSummary",
    "ReviewAuthor",
    "ReviewCreate",
    "ReviewLikeStatus",
    "ReviewRead",
    "ReviewUpdate",
    "Token",
    "TokenPayload",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "GenreCount",
    "MonthActivity",
    "StatisticsSummary",
    "UserStatistics",
    "AchievementRead",
    "UserAchievementRead",
    "NotificationRead",
    "UnreadCount",
]