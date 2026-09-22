from fastapi import APIRouter

from app.api.v1 import (
    achievements,
    anime,
    auth,
    favorites,
    library,
    notifications,
    ratings,
    recommendations,
    reviews,
    statistics,
    users,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(anime.router)
api_router.include_router(favorites.router)
api_router.include_router(library.router)
api_router.include_router(ratings.router)
api_router.include_router(reviews.router)
api_router.include_router(statistics.router)
api_router.include_router(achievements.router)
api_router.include_router(notifications.router) 
api_router.include_router(recommendations.router)