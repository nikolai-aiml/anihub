from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.anime import Anime


class Episode(Base):
    __tablename__ = "episodes"
    __table_args__ = (
        UniqueConstraint("anime_id", "number", name="uq_episode_anime_number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    anime_id: Mapped[int] = mapped_column(
        ForeignKey("anime.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    video_url: Mapped[str] = mapped_column(String(500), nullable=False)
    thumbnail_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    anime: Mapped[Anime] = relationship(back_populates="episodes")

    def __repr__(self) -> str:
        return f"<Episode anime={self.anime_id} ep={self.number}>"