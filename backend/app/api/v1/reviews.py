from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.deps import CurrentUser, DbSession, OptionalUser
from app.schemas.review import (
    ReviewCreate,
    ReviewLikeStatus,
    ReviewRead,
    ReviewUpdate,
)
from app.services.review import ReviewService

router = APIRouter(tags=["reviews"])


# ============ Отзывы для конкретного аниме ============

@router.get("/anime/{anime_id}/reviews", response_model=list[ReviewRead])
async def list_reviews(
    anime_id: int,
    db: DbSession,
    current_user: OptionalUser,
    sort: Annotated[str, Query(pattern="^(new|popular)$")] = "new",
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=50)] = 20,
) -> list[ReviewRead]:
    user_id = current_user.id if current_user else None
    return await ReviewService(db).list_by_anime(
        anime_id, user_id=user_id, sort=sort, page=page, size=size
    )


@router.post(
    "/anime/{anime_id}/reviews",
    response_model=ReviewRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    anime_id: int,
    data: ReviewCreate,
    current_user: CurrentUser,
    db: DbSession,
) -> ReviewRead:
    return await ReviewService(db).create(
        current_user.id, anime_id, data.text, data.rating
    )


# ============ Конкретный отзыв ============

@router.patch("/reviews/{review_id}", response_model=ReviewRead)
async def update_review(
    review_id: int,
    data: ReviewUpdate,
    current_user: CurrentUser,
    db: DbSession,
) -> ReviewRead:
    return await ReviewService(db).update(
        current_user.id, review_id, data.text, data.rating
    )


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    await ReviewService(db).remove(current_user.id, review_id)
    return None


# ============ Лайки ============

@router.post("/reviews/{review_id}/like", response_model=ReviewLikeStatus)
async def like_review(
    review_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> ReviewLikeStatus:
    result = await ReviewService(db).like(current_user.id, review_id)
    return ReviewLikeStatus(**result)


@router.delete("/reviews/{review_id}/like", response_model=ReviewLikeStatus)
async def unlike_review(
    review_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> ReviewLikeStatus:
    result = await ReviewService(db).unlike(current_user.id, review_id)
    return ReviewLikeStatus(**result)