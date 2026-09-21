from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RatingCreate(BaseModel):
    value: int = Field(ge=1, le=10)


class RatingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    anime_id: int
    value: int
    created_at: datetime
    updated_at: datetime


class RatingSummary(BaseModel):
    """Сводка по оценкам аниме."""

    average: float
    count: int
    user_rating: int | None = None