from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.notification import NotificationRead, UnreadCount
from app.services.notification import NotificationService

router = APIRouter(prefix="/users/me/notifications", tags=["notifications"])


@router.get("", response_model=list[NotificationRead])
async def list_notifications(
    current_user: CurrentUser,
    db: DbSession,
) -> list[NotificationRead]:
    return await NotificationService(db).list(current_user.id)


@router.get("/unread-count", response_model=UnreadCount)
async def unread_count(
    current_user: CurrentUser,
    db: DbSession,
) -> UnreadCount:
    count = await NotificationService(db).unread_count(current_user.id)
    return UnreadCount(count=count)


@router.patch("/{notification_id}/read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_read(
    notification_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    await NotificationService(db).mark_read(current_user.id, notification_id)
    return None


@router.patch("/read-all", status_code=status.HTTP_204_NO_CONTENT)
async def mark_all_read(
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    await NotificationService(db).mark_all_read(current_user.id)
    return None