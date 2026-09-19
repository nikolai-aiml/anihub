from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    db: DbSession,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if not payload or not payload.get("sub"):
        raise credentials_exc

    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError):
        raise credentials_exc

    user = await UserRepository(db).get_by_id(user_id)
    if not user:
        raise credentials_exc
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]