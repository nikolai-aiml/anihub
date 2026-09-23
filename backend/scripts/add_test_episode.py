"""Добавляет тестовый эпизод к первому аниме в БД."""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.anime import Anime
from app.models.episode import Episode


async def main():
    async with AsyncSessionLocal() as db:
        # Берём первое аниме
        result = await db.execute(select(Anime).limit(1))
        anime = result.scalar_one_or_none()
        if not anime:
            print("Нет аниме в БД")
            return

        # Проверяем, есть ли уже эпизод
        existing = await db.execute(
            select(Episode).where(Episode.anime_id == anime.id)
        )
        if existing.scalar_one_or_none():
            print("Эпизод уже есть")
            return

        # Добавляем тестовый эпизод
        episode = Episode(
            anime_id=anime.id,
            number=1,
            title="Тестовый эпизод",
            description="Это тестовый эпизод для проверки плеера.",
            video_url="/videos/test.mp4",
            duration_seconds=600,
        )
        db.add(episode)
        await db.commit()
        print(f"Добавлен эпизод 1 к '{anime.title}' (ID {anime.id})")
        print(f"Открой: http://localhost:5173/watch/{anime.id}/1")


if __name__ == "__main__":
    asyncio.run(main())