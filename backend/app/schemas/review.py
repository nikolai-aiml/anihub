from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    text: str = Field(min_length=10, max_length=2000)
    rating: int | None = Field(default=None, ge=1, le=10)


class ReviewUpdate(BaseModel):
    text: str | None = Field(default=None, min_length=10, max_length=2000)
    rating: int | None = Field(default=None, ge=1, le=10)


class ReviewAuthor(BaseModel):
    """Автор отзыва (краткая информация)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    avatar_url: str | None = None


class ReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    anime_id: int
    rating: int | None = None
    text: str
    likes_count: int
    created_at: datetime
    updated_at: datetime
    user: ReviewAuthor
    is_liked: bool = False      # лайкнул ли текущий пользователь
    is_own: bool = False        # его ли это отзыв


class ReviewLikeStatus(BaseModel):
    is_liked: bool
    likes_count: int