from __future__ import annotations

from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.anime import Anime
    from app.models.user import User


class LibraryStatus(str, PyEnum):
    PLANNED = "planned"       # Буду смотреть
    WATCHING = "watching"     # Смотрю
    COMPLETED = "completed"   # Завершено
    ON_HOLD = "on_hold"       # Отложено
    DROPPED = "dropped"       # Брошено


class LibraryEntry(Base):
    __tablename__ = "library_entries"
    __table_args__ = (
        UniqueConstraint("user_id", "anime_id", name="uq_library_user_anime"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    anime_id: Mapped[int] = mapped_column(
        ForeignKey("anime.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[LibraryStatus] = mapped_column(
        Enum(LibraryStatus, name="library_status"),
        default=LibraryStatus.PLANNED,
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="library_entries")
    anime: Mapped[Anime] = relationship()

    def __repr__(self) -> str:
        return f"<LibraryEntry user={self.user_id} anime={self.anime_id} status={self.status}>"