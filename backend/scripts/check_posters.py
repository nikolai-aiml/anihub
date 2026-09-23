"""Проверка постеров — какие URL работают, какие нет."""

import asyncio

import httpx
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.anime import Anime


async def main():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Anime.id, Anime.title, Anime.poster_url))
        rows = result.all()

        broken = []
        ok_count = 0

        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            for anime_id, title, url in rows:
                if not url:
                    broken.append((anime_id, title, "НЕТ URL"))
                    continue
                try:
                    r = await client.head(url)
                    if r.status_code != 200:
                        broken.append((anime_id, title, f"HTTP {r.status_code}"))
                    else:
                        ok_count += 1
                        print(f"OK  {title}")
                except Exception as e:
                    broken.append((anime_id, title, str(e)[:60]))

        print(f"\n=== ИТОГ ===")
        print(f"Рабочих: {ok_count}")
        print(f"Битых: {len(broken)}")

        if broken:
            print("\n=== БИТЫЕ ===")
            for anime_id, title, reason in broken:
                print(f"ID {anime_id} | {title} | {reason}")


if __name__ == "__main__":
    asyncio.run(main())