"""Замена битых URL постеров на AniList URL."""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.anime import Anime


FIXES = {
    "Берсерк": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx33-PSwfE5B0gejI.jpg",
    "Могила светлячков": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx578-vU6XcOlb1XFU.jpg",
    "Токийские мстители": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx120120-cWDmnmeEntSe.jpg",
    "Акира": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx47-4CR68arv452h.jpg",
    "Идеальная грусть": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx437-69NMlXKFeuse.jpg",
    "Гуррен-Лаганн": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx2001-XwRnjzGeFWRQ.png",
    "Бездомный бог": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx20447-EoQXeygHaVCK.jpg",
    "О моём перерождении в слизь": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx101280-tDxCVJm714nt.jpg",
    "Королевство": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx12031-1nVQa5nXPt48.png",
    "Дорохедоро": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx105228-I4xr84QS9Pvk.jpg",
    "Магическая битва 2": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx145064-hSNRJM03pvv1.jpg",
    "Кайдзю №8": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx153288-25FBfFJzEQ5O.jpg",
    "Дандадан": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx171018-60q1B6GK2Ghb.jpg",
    "Соло Левелинг": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx151807-it355ZgzquUd.png",
    "Аптекарь": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx161645-QLbzHXiYRgV2.jpg",
    "Сага о Винланде 2": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx136430-gsBsJjA7hGh9.jpg",
    "Токийские мстители: Сезон 3": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx163329-lGJRnYV9dcjc.jpg",
    "Тетрадь дружбы Нацумэ 7": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx166611-MXGsOlPv2IKj.png",
}


async def fix():
    async with AsyncSessionLocal() as db:
        fixed = 0
        not_found = 0
        for title, new_url in FIXES.items():
            result = await db.execute(select(Anime).where(Anime.title == title))
            anime = result.scalar_one_or_none()
            if anime:
                anime.poster_url = new_url
                fixed += 1
                print(f"OK  {title}")
            else:
                not_found += 1
                print(f"--  {title} (не найдено)")

        await db.commit()
        print(f"\n=== ИТОГ ===")
        print(f"Обновлено: {fixed}")
        print(f"Не найдено: {not_found}")


if __name__ == "__main__":
    asyncio.run(fix())