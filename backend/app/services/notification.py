from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification, NotificationType
from app.repositories.notification import NotificationRepository


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.notifications = NotificationRepository(db)

    async def list(self, user_id: int) -> list[Notification]:
        return await self.notifications.list_for_user(user_id)

    async def unread_count(self, user_id: int) -> int:
        return await self.notifications.count_unread(user_id)

    async def create(
        self,
        user_id: int,
        type: NotificationType,
        title: str,
        message: str,
        link: str | None = None,
    ) -> Notification:
        return await self.notifications.create(
            user_id=user_id,
            type=type,
            title=title,
            message=message,
            link=link,
        )

    async def mark_read(self, user_id: int, notification_id: int) -> None:
        await self.notifications.mark_read(user_id, notification_id)

    async def mark_all_read(self, user_id: int) -> None:
        await self.notifications.mark_all_read(user_id)

    # ============ ХЕЛПЕРЫ ДЛЯ СОБЫТИЙ ============

    async def notify_achievement(
        self, user_id: int, achievement_title: str, achievement_icon: str
    ) -> None:
        await self.create(
            user_id=user_id,
            type=NotificationType.ACHIEVEMENT,
            title="🏆 Новое достижение",
            message=f"Вы получили «{achievement_title}» {achievement_icon}",
            link="/achievements",
        )

    async def notify_review_like(
        self,
        user_id: int,
        liker_username: str,
        anime_title: str,
    ) -> None:
        await self.create(
            user_id=user_id,
            type=NotificationType.REVIEW_LIKE,
            title="👍 Лайк отзыва",
            message=f"Пользователю {liker_username} понравился ваш отзыв на «{anime_title}»",
        )