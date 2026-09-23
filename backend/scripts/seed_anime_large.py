"""Seed реальных аниме с постерами. Запуск: docker compose exec backend python -m scripts.seed_anime_large"""

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
    ("Isekai", "isekai"),
    ("Music", "music"),
    ("School", "school"),
    ("Historical", "historical"),
    ("Military", "military"),
    ("Shounen", "shounen"),
    ("Shoujo", "shoujo"),
]


# Каждая запись — словарь. Поля: title, title_en, year, type, episodes, studio, rating, poster, genres
ANIME_LIST = [
    {"title": "Атака титанов", "title_en": "Attack on Titan", "year": 2013, "type": "tv", "episodes": 87, "studio": "MAPPA", "rating": 9.0, "poster": "https://cdn.myanimelist.net/images/anime/10/47347.jpg", "genres": ["action", "drama", "fantasy"]},
    {"title": "Тетрадь смерти", "title_en": "Death Note", "year": 2006, "type": "tv", "episodes": 37, "studio": "Madhouse", "rating": 8.9, "poster": "https://cdn.myanimelist.net/images/anime/9/9453.jpg", "genres": ["psychological", "thriller", "mystery"]},
    {"title": "Стальной алхимик: Братство", "title_en": "Fullmetal Alchemist: Brotherhood", "year": 2009, "type": "tv", "episodes": 64, "studio": "Bones", "rating": 9.1, "poster": "https://cdn.myanimelist.net/images/anime/1208/94745.jpg", "genres": ["action", "adventure", "drama", "fantasy"]},
    {"title": "Ван-Пис", "title_en": "One Piece", "year": 1999, "type": "tv", "episodes": 1100, "studio": "Toei Animation", "rating": 8.7, "poster": "https://cdn.myanimelist.net/images/anime/6/73245.jpg", "genres": ["action", "adventure", "comedy", "fantasy"]},
    {"title": "Наруто", "title_en": "Naruto", "year": 2002, "type": "tv", "episodes": 220, "studio": "Pierrot", "rating": 8.4, "poster": "https://cdn.myanimelist.net/images/anime/13/17405.jpg", "genres": ["action", "adventure", "comedy"]},
    {"title": "Ковбой Бибоп", "title_en": "Cowboy Bebop", "year": 1998, "type": "tv", "episodes": 26, "studio": "Sunrise", "rating": 8.9, "poster": "https://cdn.myanimelist.net/images/anime/4/19644.jpg", "genres": ["action", "sci-fi", "drama"]},
    {"title": "Евангелион", "title_en": "Neon Genesis Evangelion", "year": 1995, "type": "tv", "episodes": 26, "studio": "Gainax", "rating": 8.5, "poster": "https://cdn.myanimelist.net/images/anime/1314/108941.jpg", "genres": ["mecha", "psychological", "drama", "sci-fi"]},
    {"title": "Хантер х Хантер", "title_en": "Hunter x Hunter", "year": 2011, "type": "tv", "episodes": 148, "studio": "Madhouse", "rating": 9.0, "poster": "https://cdn.myanimelist.net/images/anime/11/33657.jpg", "genres": ["action", "adventure", "fantasy"]},
    {"title": "Берсерк", "title_en": "Berserk", "year": 1997, "type": "tv", "episodes": 25, "studio": "OLM", "rating": 8.6, "poster": "https://cdn.myanimelist.net/images/anime/1384/119999.jpg", "genres": ["action", "adventure", "drama", "horror"]},
    {"title": "Блич", "title_en": "Bleach", "year": 2004, "type": "tv", "episodes": 366, "studio": "Pierrot", "rating": 8.2, "poster": "https://cdn.myanimelist.net/images/anime/3/40451.jpg", "genres": ["action", "adventure", "supernatural"]},
    {"title": "Унесённые призраками", "title_en": "Spirited Away", "year": 2001, "type": "movie", "episodes": 1, "studio": "Studio Ghibli", "rating": 8.6, "poster": "https://cdn.myanimelist.net/images/anime/6/79597.jpg", "genres": ["adventure", "fantasy", "supernatural"]},
    {"title": "Мой сосед Тоторо", "title_en": "My Neighbor Totoro", "year": 1988, "type": "movie", "episodes": 1, "studio": "Studio Ghibli", "rating": 8.2, "poster": "https://cdn.myanimelist.net/images/anime/4/75923.jpg", "genres": ["adventure", "fantasy", "slice-of-life"]},
    {"title": "Ходячий замок", "title_en": "Howl's Moving Castle", "year": 2004, "type": "movie", "episodes": 1, "studio": "Studio Ghibli", "rating": 8.7, "poster": "https://cdn.myanimelist.net/images/anime/5/75810.jpg", "genres": ["adventure", "fantasy", "romance"]},
    {"title": "Принцесса Мононоке", "title_en": "Princess Mononoke", "year": 1997, "type": "movie", "episodes": 1, "studio": "Studio Ghibli", "rating": 8.4, "poster": "https://cdn.myanimelist.net/images/anime/7/75919.jpg", "genres": ["adventure", "fantasy", "historical"]},
    {"title": "Могила светлячков", "title_en": "Grave of the Fireflies", "year": 1988, "type": "movie", "episodes": 1, "studio": "Studio Ghibli", "rating": 8.5, "poster": "https://cdn.myanimelist.net/images/anime/4/75814.jpg", "genres": ["drama", "historical", "military"]},
    {"title": "Клинок, рассекающий демонов", "title_en": "Demon Slayer", "year": 2019, "type": "tv", "episodes": 55, "studio": "ufotable", "rating": 8.8, "poster": "https://cdn.myanimelist.net/images/anime/1286/99889.jpg", "genres": ["action", "supernatural", "fantasy"]},
    {"title": "Моя геройская академия", "title_en": "My Hero Academia", "year": 2016, "type": "tv", "episodes": 150, "studio": "Bones", "rating": 8.0, "poster": "https://cdn.myanimelist.net/images/anime/10/78745.jpg", "genres": ["action", "adventure", "comedy"]},
    {"title": "Магическая битва", "title_en": "Jujutsu Kaisen", "year": 2020, "type": "tv", "episodes": 47, "studio": "MAPPA", "rating": 8.9, "poster": "https://cdn.myanimelist.net/images/anime/1171/109222.jpg", "genres": ["action", "supernatural", "school"]},
    {"title": "Человек-бензопила", "title_en": "Chainsaw Man", "year": 2022, "type": "tv", "episodes": 12, "studio": "MAPPA", "rating": 8.6, "poster": "https://cdn.myanimelist.net/images/anime/1806/126216.jpg", "genres": ["action", "horror", "supernatural"]},
    {"title": "Ванпанчмен", "title_en": "One Punch Man", "year": 2015, "type": "tv", "episodes": 24, "studio": "Madhouse", "rating": 8.7, "poster": "https://cdn.myanimelist.net/images/anime/12/76049.jpg", "genres": ["action", "comedy", "supernatural"]},
    {"title": "Токийский гуль", "title_en": "Tokyo Ghoul", "year": 2014, "type": "tv", "episodes": 12, "studio": "Pierrot", "rating": 7.9, "poster": "https://cdn.myanimelist.net/images/anime/5/64449.jpg", "genres": ["action", "horror", "psychological"]},
    {"title": "Волейбол!!", "title_en": "Haikyuu!!", "year": 2014, "type": "tv", "episodes": 85, "studio": "Production I.G", "rating": 8.7, "poster": "https://cdn.myanimelist.net/images/anime/7/76014.jpg", "genres": ["sports", "comedy", "drama"]},
    {"title": "Токийские мстители", "title_en": "Tokyo Revengers", "year": 2021, "type": "tv", "episodes": 37, "studio": "LIDEN FILMS", "rating": 8.0, "poster": "https://cdn.myanimelist.net/images/anime/1839/112794.jpg", "genres": ["action", "drama", "school"]},
    {"title": "Гинтама", "title_en": "Gintama", "year": 2006, "type": "tv", "episodes": 367, "studio": "Sunrise", "rating": 8.9, "poster": "https://cdn.myanimelist.net/images/anime/10/73274.jpg", "genres": ["action", "comedy", "sci-fi"]},
    {"title": "Великий из бродячих псов", "title_en": "Bungo Stray Dogs", "year": 2016, "type": "tv", "episodes": 60, "studio": "Bones", "rating": 8.0, "poster": "https://cdn.myanimelist.net/images/anime/3/79409.jpg", "genres": ["action", "mystery", "supernatural"]},
    {"title": "Твоя апрельская ложь", "title_en": "Your Lie in April", "year": 2014, "type": "tv", "episodes": 22, "studio": "A-1 Pictures", "rating": 8.6, "poster": "https://cdn.myanimelist.net/images/anime/3/67177.jpg", "genres": ["drama", "music", "romance"]},
    {"title": "Твоё имя", "title_en": "Your Name", "year": 2016, "type": "movie", "episodes": 1, "studio": "CoMix Wave Films", "rating": 8.5, "poster": "https://cdn.myanimelist.net/images/anime/5/87048.jpg", "genres": ["romance", "drama", "supernatural"]},
    {"title": "Форма голоса", "title_en": "A Silent Voice", "year": 2016, "type": "movie", "episodes": 1, "studio": "Kyoto Animation", "rating": 8.9, "poster": "https://cdn.myanimelist.net/images/anime/1122/96435.jpg", "genres": ["drama", "romance", "school"]},
    {"title": "Сад слов", "title_en": "The Garden of Words", "year": 2013, "type": "movie", "episodes": 1, "studio": "CoMix Wave Films", "rating": 8.2, "poster": "https://cdn.myanimelist.net/images/anime/6/49237.jpg", "genres": ["romance", "drama", "slice-of-life"]},
    {"title": "5 сантиметров в секунду", "title_en": "5 Centimeters per Second", "year": 2007, "type": "movie", "episodes": 1, "studio": "CoMix Wave Films", "rating": 8.0, "poster": "https://cdn.myanimelist.net/images/anime/1410/112994.jpg", "genres": ["romance", "drama", "slice-of-life"]},
    {"title": "Хоримия", "title_en": "Horimiya", "year": 2021, "type": "tv", "episodes": 13, "studio": "CloverWorks", "rating": 8.2, "poster": "https://cdn.myanimelist.net/images/anime/1695/111486.jpg", "genres": ["comedy", "romance", "school"]},
    {"title": "Госпожа Кагуя", "title_en": "Kaguya-sama: Love is War", "year": 2019, "type": "tv", "episodes": 37, "studio": "A-1 Pictures", "rating": 8.6, "poster": "https://cdn.myanimelist.net/images/anime/1295/106551.jpg", "genres": ["comedy", "psychological", "romance", "school"]},
    {"title": "Монстр", "title_en": "Monster", "year": 2004, "type": "tv", "episodes": 74, "studio": "Madhouse", "rating": 8.9, "poster": "https://cdn.myanimelist.net/images/anime/10/18793.jpg", "genres": ["psychological", "thriller", "mystery"]},
    {"title": "Психопаспорт", "title_en": "Psycho-Pass", "year": 2012, "type": "tv", "episodes": 22, "studio": "Production I.G", "rating": 8.3, "poster": "https://cdn.myanimelist.net/images/anime/1314/108941.jpg", "genres": ["sci-fi", "psychological", "thriller"]},
    {"title": "Странники", "title_en": "Steins;Gate", "year": 2011, "type": "tv", "episodes": 24, "studio": "White Fox", "rating": 9.0, "poster": "https://cdn.myanimelist.net/images/anime/5/73199.jpg", "genres": ["sci-fi", "psychological", "thriller"]},
    {"title": "Паразит", "title_en": "Parasyte", "year": 2014, "type": "tv", "episodes": 24, "studio": "Madhouse", "rating": 8.4, "poster": "https://cdn.myanimelist.net/images/anime/3/73178.jpg", "genres": ["action", "horror", "psychological", "sci-fi"]},
    {"title": "Акира", "title_en": "Akira", "year": 1988, "type": "movie", "episodes": 1, "studio": "TMS Entertainment", "rating": 8.2, "poster": "https://cdn.myanimelist.net/images/anime/5/13475.jpg", "genres": ["action", "sci-fi", "psychological"]},
    {"title": "Призрак в доспехах", "title_en": "Ghost in the Shell", "year": 1995, "type": "movie", "episodes": 1, "studio": "Production I.G", "rating": 8.3, "poster": "https://cdn.myanimelist.net/images/anime/10/82594.jpg", "genres": ["action", "sci-fi", "psychological"]},
    {"title": "Идеальная грусть", "title_en": "Perfect Blue", "year": 1997, "type": "movie", "episodes": 1, "studio": "Madhouse", "rating": 8.5, "poster": "https://cdn.myanimelist.net/images/anime/1254/116293.jpg", "genres": ["psychological", "thriller"]},
    {"title": "Код Гиас", "title_en": "Code Geass", "year": 2006, "type": "tv", "episodes": 50, "studio": "Sunrise", "rating": 8.7, "poster": "https://cdn.myanimelist.net/images/anime/5/50331.jpg", "genres": ["action", "mecha", "psychological", "sci-fi"]},
    {"title": "Гуррен-Лаганн", "title_en": "Gurren Lagann", "year": 2007, "type": "tv", "episodes": 27, "studio": "Gainax", "rating": 8.4, "poster": "https://cdn.myanimelist.net/images/anime/9/75624.jpg", "genres": ["action", "adventure", "mecha", "sci-fi"]},
    {"title": "Моб Психо 100", "title_en": "Mob Psycho 100", "year": 2016, "type": "tv", "episodes": 37, "studio": "Bones", "rating": 8.7, "poster": "https://cdn.myanimelist.net/images/anime/8/80356.jpg", "genres": ["action", "comedy", "supernatural"]},
    {"title": "Бездомный бог", "title_en": "Noragami", "year": 2014, "type": "tv", "episodes": 25, "studio": "Bones", "rating": 8.0, "poster": "https://cdn.myanimelist.net/images/anime/1886/128214.jpg", "genres": ["action", "adventure", "supernatural"]},
    {"title": "Мастера меча онлайн", "title_en": "Sword Art Online", "year": 2012, "type": "tv", "episodes": 96, "studio": "A-1 Pictures", "rating": 7.2, "poster": "https://cdn.myanimelist.net/images/anime/11/39717.jpg", "genres": ["action", "adventure", "fantasy", "isekai"]},
    {"title": "Реинкарнация безработного", "title_en": "Mushoku Tensei", "year": 2021, "type": "tv", "episodes": 23, "studio": "Studio Bind", "rating": 8.5, "poster": "https://cdn.myanimelist.net/images/anime/1530/117776.jpg", "genres": ["adventure", "drama", "fantasy", "isekai"]},
    {"title": "О моём перерождении в слизь", "title_en": "That Time I Got Reincarnated as a Slime", "year": 2018, "type": "tv", "episodes": 48, "studio": "8bit", "rating": 8.0, "poster": "https://cdn.myanimelist.net/images/anime/1275/96554.jpg", "genres": ["adventure", "comedy", "fantasy", "isekai"]},
    {"title": "Overlord", "title_en": "Overlord", "year": 2015, "type": "tv", "episodes": 52, "studio": "Madhouse", "rating": 8.0, "poster": "https://cdn.myanimelist.net/images/anime/7/88019.jpg", "genres": ["action", "adventure", "fantasy", "isekai"]},
    {"title": "Конасуба", "title_en": "KonoSuba", "year": 2016, "type": "tv", "episodes": 20, "studio": "Studio Deen", "rating": 8.1, "poster": "https://cdn.myanimelist.net/images/anime/8/77831.jpg", "genres": ["adventure", "comedy", "fantasy", "isekai"]},
    {"title": "Re:Zero", "title_en": "Re:Zero", "year": 2016, "type": "tv", "episodes": 50, "studio": "White Fox", "rating": 8.5, "poster": "https://cdn.myanimelist.net/images/anime/1522/128039.jpg", "genres": ["drama", "fantasy", "psychological", "isekai"]},
    {"title": "Королевство", "title_en": "Kingdom", "year": 2012, "type": "tv", "episodes": 138, "studio": "Pierrot", "rating": 8.5, "poster": "https://cdn.myanimelist.net/images/anime/1418/107857.jpg", "genres": ["action", "historical", "military"]},
    {"title": "Сага о Винланде", "title_en": "Vinland Saga", "year": 2019, "type": "tv", "episodes": 48, "studio": "Wit Studio", "rating": 8.8, "poster": "https://cdn.myanimelist.net/images/anime/1500/103005.jpg", "genres": ["action", "adventure", "drama", "historical"]},
    {"title": "Дорохедоро", "title_en": "Dorohedoro", "year": 2020, "type": "tv", "episodes": 12, "studio": "MAPPA", "rating": 8.1, "poster": "https://cdn.myanimelist.net/images/anime/1050/108688.jpg", "genres": ["action", "comedy", "fantasy", "horror"]},
    {"title": "Магическая битва 2", "title_en": "Jujutsu Kaisen Season 2", "year": 2023, "type": "tv", "episodes": 23, "studio": "MAPPA", "rating": 9.0, "poster": "https://cdn.myanimelist.net/images/anime/1792/138059.jpg", "genres": ["action", "supernatural", "school"]},
    {"title": "Кайдзю №8", "title_en": "Kaiju No. 8", "year": 2024, "type": "tv", "episodes": 12, "studio": "Production I.G", "rating": 8.2, "poster": "https://cdn.myanimelist.net/images/anime/1626/139749.jpg", "genres": ["action", "sci-fi"]},
    {"title": "Дандадан", "title_en": "Dandadan", "year": 2024, "type": "tv", "episodes": 12, "studio": "Science SARU", "rating": 8.5, "poster": "https://cdn.myanimelist.net/images/anime/1710/145808.jpg", "genres": ["action", "comedy", "supernatural"]},
    {"title": "Соло Левелинг", "title_en": "Solo Leveling", "year": 2024, "type": "tv", "episodes": 12, "studio": "A-1 Pictures", "rating": 8.3, "poster": "https://cdn.myanimelist.net/images/anime/1926/140516.jpg", "genres": ["action", "adventure", "fantasy"]},
    {"title": "Фрирен", "title_en": "Frieren: Beyond Journey's End", "year": 2023, "type": "tv", "episodes": 28, "studio": "Madhouse", "rating": 9.3, "poster": "https://cdn.myanimelist.net/images/anime/1015/138006.jpg", "genres": ["adventure", "drama", "fantasy"]},
    {"title": "Аптекарь", "title_en": "The Apothecary Diaries", "year": 2023, "type": "tv", "episodes": 24, "studio": "OLM", "rating": 8.8, "poster": "https://cdn.myanimelist.net/images/anime/1647/137914.jpg", "genres": ["drama", "mystery", "historical"]},
    {"title": "Сага о Винланде 2", "title_en": "Vinland Saga Season 2", "year": 2023, "type": "tv", "episodes": 24, "studio": "MAPPA", "rating": 8.9, "poster": "https://cdn.myanimelist.net/images/anime/1170/124905.jpg", "genres": ["action", "adventure", "drama", "historical"]},
    {"title": "Блич: Тысячелетняя кровавая война", "title_en": "Bleach: Thousand-Year Blood War", "year": 2022, "type": "tv", "episodes": 52, "studio": "Pierrot", "rating": 9.0, "poster": "https://cdn.myanimelist.net/images/anime/3/40451.jpg", "genres": ["action", "adventure", "supernatural"]},
    {"title": "Моб Психо 100 3", "title_en": "Mob Psycho 100 III", "year": 2022, "type": "tv", "episodes": 12, "studio": "Bones", "rating": 8.8, "poster": "https://cdn.myanimelist.net/images/anime/8/80356.jpg", "genres": ["action", "comedy", "supernatural"]},
    {"title": "Токийские мстители: Сезон 3", "title_en": "Tokyo Revengers: Tenjiku Arc", "year": 2023, "type": "tv", "episodes": 13, "studio": "LIDEN FILMS", "rating": 8.2, "poster": "https://cdn.myanimelist.net/images/anime/1839/112794.jpg", "genres": ["action", "drama", "school"]},
    {"title": "Клинок, рассекающий демонов: Тренировки столпов", "title_en": "Demon Slayer: Hashira Training Arc", "year": 2024, "type": "tv", "episodes": 8, "studio": "ufotable", "rating": 8.5, "poster": "https://cdn.myanimelist.net/images/anime/1286/99889.jpg", "genres": ["action", "supernatural", "fantasy"]},
    {"title": "Тетрадь дружбы Нацумэ 7", "title_en": "Natsume's Book of Friends Season 7", "year": 2024, "type": "tv", "episodes": 12, "studio": "Shuka", "rating": 8.7, "poster": "https://cdn.myanimelist.net/images/anime/1078/106106.jpg", "genres": ["drama", "supernatural", "slice-of-life"]},
    {"title": "Клинок, рассекающий демонов: Бесконечный поезд", "title_en": "Demon Slayer: Mugen Train", "year": 2020, "type": "movie", "episodes": 1, "studio": "ufotable", "rating": 8.7, "poster": "https://cdn.myanimelist.net/images/anime/1704/106947.jpg", "genres": ["action", "supernatural", "fantasy"]},
    {"title": "Магическая битва 0", "title_en": "Jujutsu Kaisen 0", "year": 2021, "type": "movie", "episodes": 1, "studio": "MAPPA", "rating": 8.5, "poster": "https://cdn.myanimelist.net/images/anime/1121/119428.jpg", "genres": ["action", "supernatural", "school"]},
    {"title": "Атака титанов: Финал", "title_en": "Attack on Titan: The Final Season", "year": 2020, "type": "tv", "episodes": 28, "studio": "MAPPA", "rating": 9.2, "poster": "https://cdn.myanimelist.net/images/anime/1000/110531.jpg", "genres": ["action", "drama", "fantasy"]},
    {"title": "Моя геройская академия 7", "title_en": "My Hero Academia Season 7", "year": 2024, "type": "tv", "episodes": 21, "studio": "Bones", "rating": 8.2, "poster": "https://cdn.myanimelist.net/images/anime/10/78745.jpg", "genres": ["action", "adventure", "school"]},
]


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        # 1. Жанры
        existing_genres_result = await db.execute(select(Genre.slug))
        existing_slugs = {row[0] for row in existing_genres_result.all()}

        new_genres = [
            Genre(name=name, slug=slug)
            for name, slug in GENRES
            if slug not in existing_slugs
        ]
        if new_genres:
            db.add_all(new_genres)
            await db.flush()
            print(f"Добавлено жанров: {len(new_genres)}")

        all_genres_result = await db.execute(select(Genre))
        genre_map = {g.slug: g for g in all_genres_result.scalars().all()}

        # 2. Аниме
        existing_titles_result = await db.execute(select(Anime.title))
        existing_titles = {row[0] for row in existing_titles_result.all()}

        added = 0
        for item in ANIME_LIST:
            if item["title"] in existing_titles:
                continue

            anime = Anime(
                title=item["title"],
                title_en=item["title_en"],
                year=item["year"],
                type=AnimeType(item["type"]),
                status=AnimeStatus.COMPLETED,
                episodes_total=item["episodes"],
                duration_minutes=24 if item["type"] == "tv" else None,
                studio=item["studio"],
                rating=item["rating"],
                rating_count=100,
                poster_url=item["poster"],
                description=f"Популярное аниме {item['title_en']} ({item['year']}).",
            )
            anime.genres = [genre_map[g] for g in item["genres"] if g in genre_map]
            db.add(anime)
            added += 1

        await db.commit()
        print(f"Добавлено аниме: {added}")
        print("Готово.")


if __name__ == "__main__":
    asyncio.run(seed())