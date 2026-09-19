from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import CurrentUser, DbSession
from app.core.security import create_access_token
from app.schemas.user import Token, UserCreate, UserRead
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: DbSession) -> UserRead:
    user = await AuthService(db).register(data)
    return user


@router.post("/login", response_model=Token)
async def login(
    db: DbSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await AuthService(db).authenticate(form_data.username, form_data.password)
    token = create_access_token(subject=user.id)
    return Token(access_token=token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(current_user: CurrentUser) -> None:
    return None