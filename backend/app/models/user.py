from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.notification import Notification
    from app.models.achievement import UserAchievement
    from app.models.favorite import Favorite
    from app.models.library import LibraryEntry
    from app.models.rating import Rating
    from app.models.review import Review


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    favorites: Mapped[list[Favorite]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    library_entries: Mapped[list[LibraryEntry]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    ratings: Mapped[list[Rating]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    reviews: Mapped[list[Review]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    achievements: Mapped[list[UserAchievement]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    notifications: Mapped[list[Notification]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )