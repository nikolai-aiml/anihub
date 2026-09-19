"""
Seed-скрипт: наполняет БД жанрами и тестовыми аниме.

Запуск:
    docker compose exec backend python -m scripts.seed_anime
"""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.anime import Anime, AnimeStatus, AnimeType
from app.models.genre import Genre


GENRES = [
    ("Action", "action"),
    ("Adventure", "adventure"),
    ("Comedy", "comedy"),
    ("Drama", "drama"),
    ("Fantasy", "fantasy"),
    ("Horror", "horror"),
    ("Mystery", "mystery"),
    ("Psychological", "psychological"),
    ("Romance", "romance"),
    ("Sci-Fi", "sci-fi"),
    ("Slice of Life", "slice-of-life"),
    ("Sports", "sports"),
    ("Supernatural", "supernatural"),
    ("Thriller", "thriller"),
    ("Mecha", "mecha"),
]


ANIME = [
    {
        "title": "Атака титанов",
        "title_en": "Attack on Titan",
        "title_jp": "進撃の巨人",
        "description": "Человечество живёт за огромными стенами, спасаясь от титанов — гигантских существ, пожирающих людей.",
        "year": 2013,
        "type": AnimeType.TV,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 87,
        "duration_minutes": 24,
        "studio": "MAPPA",
        "rating": 9.0,
        "rating_count": 1520,
        "genres": ["action", "drama", "fantasy"],
    },
    {
        "title": "Тетрадь смерти",
        "title_en": "Death Note",
        "title_jp": "デスノート",
        "description": "Студент находит тетрадь, в которой можно убить любого, чьё имя напишешь.",
        "year": 2006,
        "type": AnimeType.TV,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 37,
        "duration_minutes": 23,
        "studio": "Madhouse",
        "rating": 8.9,
        "rating_count": 2100,
        "genres": ["psychological", "thriller", "mystery"],
    },
    {
        "title": "Стальной алхимик: Братство",
        "title_en": "Fullmetal Alchemist: Brotherhood",
        "title_jp": "鋼の錬金術師",
        "description": "Два брата ищут философский камень, чтобы вернуть свои тела.",
        "year": 2009,
        "type": AnimeType.TV,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 64,
        "duration_minutes": 24,
        "studio": "Bones",
        "rating": 9.1,
        "rating_count": 1800,
        "genres": ["action", "adventure", "drama", "fantasy"],
    },
    {
        "title": "Ван-Пис",
        "title_en": "One Piece",
        "title_jp": "ワンピース",
        "description": "Луффи и его команда ищут легендарное сокровище Ван-Пис.",
        "year": 1999,
        "type": AnimeType.TV,
        "status": AnimeStatus.ONGOING,
        "episodes_total": 1100,
        "duration_minutes": 24,
        "studio": "Toei Animation",
        "rating": 8.7,
        "rating_count": 2400,
        "genres": ["action", "adventure", "comedy", "fantasy"],
    },
    {
        "title": "Наруто",
        "title_en": "Naruto",
        "title_jp": "ナルト",
        "description": "Молодой ниндзя мечтает стать Хокаге — главой своей деревни.",
        "year": 2002,
        "type": AnimeType.TV,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 220,
        "duration_minutes": 23,
        "studio": "Pierrot",
        "rating": 8.4,
        "rating_count": 1650,
        "genres": ["action", "adventure", "comedy"],
    },
    {
        "title": "Унесённые призраками",
        "title_en": "Spirited Away",
        "title_jp": "千と千尋の神隠し",
        "description": "Девочка попадает в мир духов и должна спасти своих родителей.",
        "year": 2001,
        "type": AnimeType.MOVIE,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 1,
        "duration_minutes": 125,
        "studio": "Studio Ghibli",
        "rating": 8.6,
        "rating_count": 1300,
        "genres": ["adventure", "fantasy", "supernatural"],
    },
    {
        "title": "Мой сосед Тоторо",
        "title_en": "My Neighbor Totoro",
        "title_jp": "となりのトトロ",
        "description": "Две сестры подружились с лесными духами.",
        "year": 1988,
        "type": AnimeType.MOVIE,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 1,
        "duration_minutes": 86,
        "studio": "Studio Ghibli",
        "rating": 8.2,
        "rating_count": 900,
        "genres": ["adventure", "fantasy", "slice-of-life"],
    },
    {
        "title": "Твоё имя",
        "title_en": "Your Name",
        "title_jp": "君の名は。",
        "description": "Парень и девушка меняются телами во сне.",
        "year": 2016,
        "type": AnimeType.MOVIE,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 1,
        "duration_minutes": 106,
        "studio": "CoMix Wave Films",
        "rating": 8.5,
        "rating_count": 1450,
        "genres": ["romance", "drama", "supernatural"],
    },
    {
        "title": "Клинок, рассекающий демонов",
        "title_en": "Demon Slayer",
        "title_jp": "鬼滅の刃",
        "description": "Танджиро становится охотником на демонов, чтобы спасти сестру.",
        "year": 2019,
        "type": AnimeType.TV,
        "status": AnimeStatus.ONGOING,
        "episodes_total": 55,
        "duration_minutes": 24,
        "studio": "ufotable",
        "rating": 8.8,
        "rating_count": 1900,
        "genres": ["action", "supernatural", "fantasy"],
    },
    {
        "title": "Моя геройская академия",
        "title_en": "My Hero Academia",
        "title_jp": "僕のヒーローアカデミア",
        "description": "Мальчик без причуды мечтает стать героем.",
        "year": 2016,
        "type": AnimeType.TV,
        "status": AnimeStatus.ONGOING,
        "episodes_total": 150,
        "duration_minutes": 24,
        "studio": "Bones",
        "rating": 8.0,
        "rating_count": 1100,
        "genres": ["action", "adventure", "comedy"],
    },
    {
        "title": "Евангелион",
        "title_en": "Neon Genesis Evangelion",
        "title_jp": "新世紀エヴァンゲリオン",
        "description": "Подростки пилотируют биомеханических роботов против Ангелов.",
        "year": 1995,
        "type": AnimeType.TV,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 26,
        "duration_minutes": 24,
        "studio": "Gainax",
        "rating": 8.5,
        "rating_count": 1050,
        "genres": ["mecha", "psychological", "drama", "sci-fi"],
    },
    {
        "title": "Ковбой Бибоп",
        "title_en": "Cowboy Bebop",
        "title_jp": "カウボーイビバップ",
        "description": "Команда охотников за головами путешествует по космосу.",
        "year": 1998,
        "type": AnimeType.TV,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 26,
        "duration_minutes": 24,
        "studio": "Sunrise",
        "rating": 8.9,
        "rating_count": 1250,
        "genres": ["action", "sci-fi", "drama"],
    },
    {
        "title": "Ванпанчмен",
        "title_en": "One Punch Man",
        "title_jp": "ワンパンマン",
        "description": "Герой, побеждающий любого врага одним ударом, скучает.",
        "year": 2015,
        "type": AnimeType.TV,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 24,
        "duration_minutes": 24,
        "studio": "Madhouse",
        "rating": 8.7,
        "rating_count": 1700,
        "genres": ["action", "comedy", "supernatural"],
    },
    {
        "title": "Хеталия",
        "title_en": "Hetalia",
        "title_jp": "ヘタリア",
        "description": "Персонификация стран в комедийном ключе.",
        "year": 2009,
        "type": AnimeType.ONA,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 52,
        "duration_minutes": 5,
        "studio": "Studio Deen",
        "rating": 7.5,
        "rating_count": 350,
        "genres": ["comedy", "slice-of-life"],
    },
    {
        "title": "Психопаспорт",
        "title_en": "Psycho-Pass",
        "title_jp": "PSYCHO-PASS サイコパス",
        "description": "В будущем преступность предсказывают до её совершения.",
        "year": 2012,
        "type": AnimeType.TV,
        "status": AnimeStatus.COMPLETED,
        "episodes_total": 22,
        "duration_minutes": 24,
        "studio": "Production I.G",
        "rating": 8.3,
        "rating_count": 780,
        "genres": ["sci-fi", "psychological", "thriller"],
    },
]


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        # 1. Жанры
        existing_genres = await db.execute(select(Genre.slug))
        existing_slugs = {row[0] for row in existing_genres.all()}

        new_genres = [
            Genre(name=name, slug=slug)
            for name, slug in GENRES
            if slug not in existing_slugs
        ]
        if new_genres:
            db.add_all(new_genres)
            await db.flush()
            print(f"Добавлено жанров: {len(new_genres)}")
        else:
            print("Жанры уже есть")

        # 2. Аниме
        existing_titles = await db.execute(select(Anime.title))
        existing_titles_set = {row[0] for row in existing_titles.all()}

        # Загружаем все жанры в dict {slug: Genre}
        all_genres = await db.execute(select(Genre))
        genre_map = {g.slug: g for g in all_genres.scalars().all()}

        added_anime = 0
        for data in ANIME:
            if data["title"] in existing_titles_set:
                continue

            genre_slugs = data.pop("genres")
            anime = Anime(**data)
            anime.genres = [genre_map[s] for s in genre_slugs if s in genre_map]
            db.add(anime)
            added_anime += 1

        await db.commit()
        print(f"Добавлено аниме: {added_anime}")
        print("Готово.")


if __name__ == "__main__":
    asyncio.run(seed())