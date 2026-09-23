from __future__ import annotations

from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    Column,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.episode import Episode
    from app.models.genre import Genre
    from app.models.rating import Rating
    from app.models.review import Review
    from app.models.genre import Genre
    from app.models.genre import Genre
    from app.models.rating import Rating
    from app.models.genre import Genre
    from app.models.rating import Rating
    from app.models.review import Review

anime_genres = Table(
    "anime_genres",
    Base.metadata,
    Column("anime_id", ForeignKey("anime.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)


class AnimeType(str, PyEnum):
    TV = "tv"
    MOVIE = "movie"
    OVA = "ova"
    ONA = "ona"
    SPECIAL = "special"


class AnimeStatus(str, PyEnum):
    ONGOING = "ongoing"
    COMPLETED = "completed"
    UPCOMING = "upcoming"


class Anime(Base):
    __tablename__ = "anime"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    title_en: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    title_jp: Mapped[str | None] = mapped_column(String(255), nullable=True)
    alternative_titles: Mapped[str | None] = mapped_column(Text, nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    poster_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    year: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    type: Mapped[AnimeType] = mapped_column(
        Enum(AnimeType, name="anime_type"), default=AnimeType.TV, nullable=False
    )
    status: Mapped[AnimeStatus] = mapped_column(
        Enum(AnimeStatus, name="anime_status"),
        default=AnimeStatus.COMPLETED,
        nullable=False,
    )
    episodes_total: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    studio: Mapped[str | None] = mapped_column(String(150), nullable=True)

    rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rating_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    genres: Mapped[list[Genre]] = relationship(
        secondary="anime_genres",
        back_populates="anime",
        lazy="selectin",
    )
    ratings: Mapped[list[Rating]] = relationship(
        back_populates="anime",
        cascade="all, delete-orphan",
    )
    reviews: Mapped[list[Review]] = relationship(
        back_populates="anime",
        cascade="all, delete-orphan",
    )
    episodes: Mapped[list[Episode]] = relationship(
        back_populates="anime",
        cascade="all, delete-orphan",
        order_by="Episode.number",
    )

    def __repr__(self) -> str:
        return f"<Anime {self.title}>"