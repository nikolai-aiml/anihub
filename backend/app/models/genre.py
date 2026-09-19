from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.anime import Anime


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    slug: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )

    anime: Mapped[list[Anime]] = relationship(
        secondary="anime_genres",
        back_populates="genres",
    )

    def __repr__(self) -> str:
        return f"<Genre {self.name}>"