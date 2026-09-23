from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EpisodeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    anime_id: int
    number: int
    title: str | None = None
    description: str | None = None
    video_url: str
    thumbnail_url: str | None = None
    duration_seconds: int | None = None
    created_at: datetime