"""
Fixtures для тестов.
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.database import Base, get_db
from app.core.security import hash_password
from app.main import app
from app.models.anime import Anime, AnimeStatus, AnimeType
from app.models.user import User

# Тестовая БД (SQLite in-memory для скорости)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Event loop для всей сессии тестов."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Движок тестовой БД — создаётся заново для каждого теста."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Сессия БД для теста."""
    session_factory = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP-клиент с подменённой БД."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# ============ ХЕЛПЕРЫ ============

async def create_test_user(
    db: AsyncSession,
    username: str = "testuser",
    email: str = "test@example.com",
    password: str = "test12345",
) -> User:
    """Создаёт пользователя в БД."""
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_test_anime(
    db: AsyncSession,
    title: str = "Test Anime",
    year: int = 2020,
    rating: float = 8.5,
    rating_count: int = 100,
) -> Anime:
    """Создаёт аниме в БД."""
    anime = Anime(
        title=title,
        title_en=title,
        year=year,
        type=AnimeType.TV,
        status=AnimeStatus.COMPLETED,
        episodes_total=12,
        rating=rating,
        rating_count=rating_count,
    )
    db.add(anime)
    await db.commit()
    await db.refresh(anime)
    return anime


async def login_user(
    client: AsyncClient,
    username: str = "testuser",
    password: str = "test12345",
) -> str:
    """Логинится и возвращает access_token."""
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


async def auth_headers(
    client: AsyncClient,
    username: str = "testuser",
    password: str = "test12345",
) -> dict:
    """Возвращает headers с Bearer-токеном."""
    token = await login_user(client, username, password)
    return {"Authorization": f"Bearer {token}"}


# ============ FIXTURES С ПОЛЬЗОВАТЕЛЯМИ ============

@pytest_asyncio.fixture
async def user(db_session: AsyncSession) -> User:
    """Тестовый пользователь."""
    return await create_test_user(db_session)


@pytest_asyncio.fixture
async def user2(db_session: AsyncSession) -> User:
    """Второй пользователь (для тестов доступа)."""
    return await create_test_user(
        db_session,
        username="user2",
        email="user2@example.com",
        password="test12345",
    )


@pytest_asyncio.fixture
async def anime(db_session: AsyncSession) -> Anime:
    """Тестовое аниме."""
    return await create_test_anime(db_session)


@pytest_asyncio.fixture
async def user_headers(client: AsyncClient, user: User) -> dict:
    """Headers первого пользователя."""
    return await auth_headers(client)


@pytest_asyncio.fixture
async def user2_headers(client: AsyncClient, user2: User) -> dict:
    """Headers второго пользователя."""
    return await auth_headers(client, "user2", "test12345")