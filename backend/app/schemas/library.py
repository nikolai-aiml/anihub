from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.library import LibraryStatus
from app.schemas.anime import AnimeListItem


class LibraryEntryCreate(BaseModel):
    status: LibraryStatus = LibraryStatus.PLANNED


class LibraryEntryUpdate(BaseModel):
    status: LibraryStatus


class LibraryEntryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    anime_id: int
    status: LibraryStatus
    created_at: datetime
    updated_at: datetime
    anime: AnimeListItem