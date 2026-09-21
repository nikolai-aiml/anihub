from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.deps import CurrentUser, DbSession
from app.models.library import LibraryStatus
from app.schemas.library import (
    LibraryEntryCreate,
    LibraryEntryRead,
    LibraryEntryUpdate,
)
from app.services.library import LibraryService

router = APIRouter(prefix="/users/me/library", tags=["library"])


@router.get("", response_model=list[LibraryEntryRead])
async def list_library(
    current_user: CurrentUser,
    db: DbSession,
    status_filter: Annotated[LibraryStatus | None, Query(alias="status")] = None,
) -> list[LibraryEntryRead]:
    return await LibraryService(db).list_library(current_user.id, status_filter)


@router.get("/stats")
async def library_stats(
    current_user: CurrentUser,
    db: DbSession,
) -> dict[str, int]:
    return await LibraryService(db).get_status_counts(current_user.id)


@router.post(
    "/{anime_id}",
    response_model=LibraryEntryRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_to_library(
    anime_id: int,
    data: LibraryEntryCreate,
    current_user: CurrentUser,
    db: DbSession,
) -> LibraryEntryRead:
    return await LibraryService(db).add_to_library(
        current_user.id, anime_id, data.status
    )


@router.patch("/{anime_id}", response_model=LibraryEntryRead)
async def update_library_status(
    anime_id: int,
    data: LibraryEntryUpdate,
    current_user: CurrentUser,
    db: DbSession,
) -> LibraryEntryRead:
    return await LibraryService(db).update_status(
        current_user.id, anime_id, data.status
    )


@router.delete("/{anime_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_library(
    anime_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    await LibraryService(db).remove_from_library(current_user.id, anime_id)
    return None