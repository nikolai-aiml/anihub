"""
Расширенный seed: 200+ аниме (100 реальных + 100 сгенерированных).

Запуск:
    docker compose exec backend python -m scripts.seed_anime_large
"""

import asyncio
import random

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.anime import Anime, AnimeStatus, AnimeType
from app.models.genre import Genre


# ============ ЖАНРЫ (25) ============
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
    ("Demons", "demons"),
    ("Magic", "magic"),
    ("Seinen", "seinen"),
    ("Shounen", "shounen"),
    ("Shoujo", "shoujo"),
]


# ============ РЕАЛЬНЫЕ АНИМЕ (100) ============
# Формат: (title, title_en, year, type, episodes, studio, rating, [genres])
REAL_ANIME = [
    ("Атака титанов", "Attack on Titan", 2013, "tv", 87, "MAPPA", 9.0, ["action", "drama", "fantasy"]),
    ("Тетрадь смерти", "Death Note", 2006, "tv", 37, "Madhouse", 8.9, ["psychological", "thriller", "mystery"]),
    ("Стальной алхимик: Братство", "Fullmetal Alchemist: Brotherhood", 2009, "tv", 64, "Bones", 9.1, ["action", "adventure", "drama", "fantasy"]),
    ("Ван-Пис", "One Piece", 1999, "tv", 1100, "Toei Animation", 8.7, ["action", "adventure", "comedy", "fantasy"]),
    ("Наруто", "Naruto", 2002, "tv", 220, "Pierrot", 8.4, ["action", "adventure", "comedy"]),
    ("Наруто: Ураганные хроники", "Naruto Shippuden", 2007, "tv", 500, "Pierrot", 8.6, ["action", "adventure", "drama"]),
    ("Блич", "Bleach", 2004, "tv", 366, "Pierrot", 8.2, ["action", "adventure", "supernatural"]),
    ("Ковбой Бибоп", "Cowboy Bebop", 1998, "tv", 26, "Sunrise", 8.9, ["action", "sci-fi", "drama"]),
    ("Евангелион", "Neon Genesis Evangelion", 1995, "tv", 26, "Gainax", 8.5, ["mecha", "psychological", "drama", "sci-fi"]),
    ("Легенда о героях Галактики", "Legend of the Galactic Heroes", 1988, "ova", 110, "Artland", 9.0, ["sci-fi", "drama", "military"]),
    ("Клинок, рассекающий демонов", "Demon Slayer", 2019, "tv", 55, "ufotable", 8.8, ["action", "supernatural", "fantasy"]),
    ("Моя геройская академия", "My Hero Academia", 2016, "tv", 150, "Bones", 8.0, ["action", "adventure", "comedy"]),
    ("Магическая битва", "Jujutsu Kaisen", 2020, "tv", 47, "MAPPA", 8.9, ["action", "supernatural", "school"]),
    ("Человек-бензопила", "Chainsaw Man", 2022, "tv", 12, "MAPPA", 8.6, ["action", "horror", "supernatural"]),
    ("Ванпанчмен", "One Punch Man", 2015, "tv", 24, "Madhouse", 8.7, ["action", "comedy", "supernatural"]),
    ("Токийский гуль", "Tokyo Ghoul", 2014, "tv", 12, "Pierrot", 7.9, ["action", "horror", "psychological"]),
    ("Клеймор", "Claymore", 2007, "tv", 26, "Madhouse", 8.0, ["action", "adventure", "fantasy"]),
    ("Хантер х Хантер", "Hunter x Hunter", 2011, "tv", 148, "Madhouse", 9.0, ["action", "adventure", "fantasy"]),
    ("Берсерк", "Berserk", 1997, "tv", 25, "OLM", 8.6, ["action", "adventure", "drama", "horror"]),
    ("Семь смертных грехов", "The Seven Deadly Sins", 2014, "tv", 96, "A-1 Pictures", 7.7, ["action", "adventure", "fantasy"]),
    ("Волейбол!!", "Haikyuu!!", 2014, "tv", 85, "Production I.G", 8.7, ["sports", "comedy", "drama"]),
    ("Куроко-но баскет", "Kuroko's Basketball", 2012, "tv", 75, "Production I.G", 8.3, ["sports", "school"]),
    ("Бегун из Слабого", "Yowamushi Pedal", 2013, "tv", 62, "TMS Entertainment", 8.0, ["sports", "comedy"]),
    ("Король-шаман", "Slam Dunk", 1993, "tv", 101, "Toei Animation", 8.7, ["sports", "comedy", "drama"]),
    ("Свобода! Плавание", "Free!", 2013, "tv", 37, "Kyoto Animation", 7.5, ["sports", "school"]),
    ("Сейлор Мун", "Sailor Moon", 1992, "tv", 200, "Toei Animation", 7.7, ["magic", "romance", "shoujo"]),
    ("Карточки Сакуры", "Cardcaptor Sakura", 1998, "tv", 70, "Madhouse", 8.2, ["magic", "romance", "shoujo"]),
    ("Фрукты корзины", "Fruits Basket", 2019, "tv", 63, "TMS Entertainment", 8.6, ["romance", "drama", "shoujo"]),
    ("Ваншот", "Ouran High School Host Club", 2006, "tv", 26, "Bones", 8.2, ["comedy", "romance", "school", "shoujo"]),
    ("Твоя апрельская ложь", "Your Lie in April", 2014, "tv", 22, "A-1 Pictures", 8.6, ["drama", "music", "romance"]),
    ("Твоё имя", "Your Name", 2016, "movie", 1, "CoMix Wave Films", 8.5, ["romance", "drama", "supernatural"]),
    ("Унесённые призраками", "Spirited Away", 2001, "movie", 1, "Studio Ghibli", 8.6, ["adventure", "fantasy", "supernatural"]),
    ("Мой сосед Тоторо", "My Neighbor Totoro", 1988, "movie", 1, "Studio Ghibli", 8.2, ["adventure", "fantasy", "slice-of-life"]),
    ("Ходячий замок", "Howl's Moving Castle", 2004, "movie", 1, "Studio Ghibli", 8.7, ["adventure", "fantasy", "romance"]),
    ("Принцесса Мононоке", "Princess Mononoke", 1997, "movie", 1, "Studio Ghibli", 8.4, ["adventure", "fantasy", "historical"]),
    ("Ветер крепчает", "The Wind Rises", 2013, "movie", 1, "Studio Ghibli", 8.1, ["drama", "historical", "romance"]),
    ("Форма голоса", "A Silent Voice", 2016, "movie", 1, "Kyoto Animation", 8.9, ["drama", "romance", "school"]),
    ("Сад слов", "The Garden of Words", 2013, "movie", 1, "CoMix Wave Films", 8.2, ["romance", "drama", "slice-of-life"]),
    ("5 сантиметров в секунду", "5 Centimeters per Second", 2007, "movie", 1, "CoMix Wave Films", 8.0, ["romance", "drama", "slice-of-life"]),
    ("Потерянные звёзды", "Children Who Chase Lost Voices", 2011, "movie", 1, "CoMix Wave Films", 7.8, ["adventure", "fantasy", "romance"]),
    ("Монстр", "Monster", 2004, "tv", 74, "Madhouse", 8.9, ["psychological", "thriller", "mystery"]),
    ("Психопаспорт", "Psycho-Pass", 2012, "tv", 22, "Production I.G", 8.3, ["sci-fi", "psychological", "thriller"]),
    ("Странники", "Steins;Gate", 2011, "tv", 24, "White Fox", 9.0, ["sci-fi", "psychological", "thriller"]),
    ("Эрго Прокси", "Ergo Proxy", 2006, "tv", 23, "Manglobe", 8.0, ["sci-fi", "psychological", "mystery"]),
    ("Паразит: Учение о жизни", "Parasyte", 2014, "tv", 24, "Madhouse", 8.4, ["action", "horror", "psychological", "sci-fi"]),
    ("Мир Тетради смерти", "Death Parade", 2015, "tv", 12, "Madhouse", 8.2, ["psychological", "drama", "mystery"]),
    ("Иная", "Another", 2012, "tv", 12, "P.A. Works", 7.7, ["horror", "mystery", "thriller"]),
    ("Мастера меча онлайн", "Sword Art Online", 2012, "tv", 96, "A-1 Pictures", 7.2, ["action", "adventure", "fantasy", "isekai"]),
    ("Реинкарнация безработного", "Mushoku Tensei", 2021, "tv", 23, "Studio Bind", 8.5, ["adventure", "drama", "fantasy", "isekai"]),
    ("О моём перерождении в слизь", "That Time I Got Reincarnated as a Slime", 2018, "tv", 48, "8bit", 8.0, ["adventure", "comedy", "fantasy", "isekai"]),
    ("Восхождение героя щита", "The Rising of the Shield Hero", 2019, "tv", 38, "Kinema Citrus", 7.9, ["action", "adventure", "fantasy", "isekai"]),
    ("Моя следующая жизнь в качестве злодейки", "My Next Life as a Villainess", 2020, "tv", 24, "Silver Link", 7.6, ["comedy", "fantasy", "isekai", "romance"]),
    ("Логин Хорайзон", "Log Horizon", 2013, "tv", 62, "Satelight", 7.9, ["adventure", "fantasy", "isekai"]),
    ("Overlord", "Overlord", 2015, "tv", 52, "Madhouse", 8.0, ["action", "adventure", "fantasy", "isekai"]),
    ("Конасуба", "KonoSuba", 2016, "tv", 20, "Studio Deen", 8.1, ["adventure", "comedy", "fantasy", "isekai"]),
    ("Re:Zero", "Re:Zero", 2016, "tv", 50, "White Fox", 8.5, ["drama", "fantasy", "psychological", "isekai"]),
    ("Акира", "Akira", 1988, "movie", 1, "TMS Entertainment", 8.2, ["action", "sci-fi", "psychological"]),
    ("Призрак в доспехах", "Ghost in the Shell", 1995, "movie", 1, "Production I.G", 8.3, ["action", "sci-fi", "psychological"]),
    ("Код Гиас", "Code Geass", 2006, "tv", 50, "Sunrise", 8.7, ["action", "mecha", "psychological", "sci-fi"]),
    ("Гуррен-Лаганн", "Gurren Lagann", 2007, "tv", 27, "Gainax", 8.4, ["action", "adventure", "mecha", "sci-fi"]),
    ("Маг: Восхождение", "Magi: The Labyrinth of Magic", 2012, "tv", 50, "A-1 Pictures", 8.0, ["action", "adventure", "fantasy"]),
    ("Тетрадь дружбы Нацумэ", "Natsume's Book of Friends", 2008, "tv", 74, "Brain's Base", 8.5, ["drama", "supernatural", "slice-of-life"]),
    ("Могила светлячков", "Grave of the Fireflies", 1988, "movie", 1, "Studio Ghibli", 8.5, ["drama", "historical", "military"]),
    ("Токийские мстители", "Tokyo Revengers", 2021, "tv", 37, "LIDEN FILMS", 8.0, ["action", "drama", "school"]),
    ("Гинтама", "Gintama", 2006, "tv", 367, "Sunrise", 8.9, ["action", "comedy", "sci-fi"]),
    ("Великий из бродячих псов", "Bungo Stray Dogs", 2016, "tv", 60, "Bones", 8.0, ["action", "mystery", "supernatural"]),
    ("Дневник будущего", "Future Diary", 2011, "tv", 26, "asread", 7.8, ["action", "psychological", "thriller"]),
    ("Бездомный бог", "Noragami", 2014, "tv", 25, "Bones", 8.0, ["action", "adventure", "supernatural"]),
    ("Кобаяши и её горничная-дракон", "Miss Kobayashi's Dragon Maid", 2017, "tv", 25, "Kyoto Animation", 8.0, ["comedy", "fantasy", "slice-of-life"]),
    ("Хоримия", "Horimiya", 2021, "tv", 13, "CloverWorks", 8.2, ["comedy", "romance", "school"]),
    ("Госпожа Кагуя", "Kaguya-sama: Love is War", 2019, "tv", 37, "A-1 Pictures", 8.6, ["comedy", "psychological", "romance", "school"]),
    ("Квартет аниме", "Monthly Girls' Nozaki-kun", 2014, "tv", 12, "Doga Kobo", 8.0, ["comedy", "romance", "school"]),
    ("Жизнь в другом мире из-за переезда", "The Devil is a Part-Timer!", 2013, "tv", 13, "White Fox", 8.0, ["comedy", "fantasy", "isekai"]),
    ("Клинок, рассекающий демонов: Бесконечный поезд", "Demon Slayer: Mugen Train", 2020, "movie", 1, "ufotable", 8.7, ["action", "supernatural", "fantasy"]),
    ("Магическая битва 0", "Jujutsu Kaisen 0", 2021, "movie", 1, "MAPPA", 8.5, ["action", "supernatural", "school"]),
    ("Атака титанов: Финал", "Attack on Titan: The Final Season", 2020, "tv", 28, "MAPPA", 9.2, ["action", "drama", "fantasy"]),
    ("Берсерк: Золотой век", "Berserk: The Golden Age Arc", 2012, "movie", 3, "Studio 4°C", 8.3, ["action", "adventure", "drama", "horror"]),
    ("Сага о Винланде", "Vinland Saga", 2019, "tv", 48, "Wit Studio", 8.8, ["action", "adventure", "drama", "historical"]),
    ("Дорохедоро", "Dorohedoro", 2020, "tv", 12, "MAPPA", 8.1, ["action", "comedy", "fantasy", "horror"]),
    ("Пианист", "Piano no Mori", 2018, "tv", 12, "Gaina", 7.8, ["drama", "music", "school"]),
    ("Кей-он!", "K-On!", 2009, "tv", 41, "Kyoto Animation", 8.0, ["comedy", "music", "school", "slice-of-life"]),
    ("Банановая рыба", "Banana Fish", 2018, "tv", 24, "MAPPA", 8.5, ["action", "drama", "thriller"]),
    ("Данганронпа", "Danganronpa", 2013, "tv", 13, "Lerche", 7.3, ["action", "mystery", "psychological", "thriller"]),
    ("Королевство", "Kingdom", 2012, "tv", 138, "Pierrot", 8.5, ["action", "historical", "military"]),
    ("Ворота: Так сражались там", "GATE", 2015, "tv", 24, "A-1 Pictures", 7.7, ["action", "adventure", "fantasy", "military"]),
    ("Дневник торговца", "Spice and Wolf", 2008, "tv", 25, "Imagin", 8.3, ["adventure", "fantasy", "romance"]),
    ("Магическая битва 2", "Jujutsu Kaisen Season 2", 2023, "tv", 23, "MAPPA", 9.0, ["action", "supernatural", "school"]),
    ("Адский рай", "Hell's Paradise", 2023, "tv", 13, "MAPPA", 8.0, ["action", "adventure", "fantasy"]),
    ("Кайдзю №8", "Kaiju No. 8", 2024, "tv", 12, "Production I.G", 8.2, ["action", "sci-fi"]),
    ("Дандадан", "Dandadan", 2024, "tv", 12, "Science SARU", 8.5, ["action", "comedy", "supernatural"]),
    ("Соло Левелинг", "Solo Leveling", 2024, "tv", 12, "A-1 Pictures", 8.3, ["action", "adventure", "fantasy"]),
    ("Фрирен", "Frieren: Beyond Journey's End", 2023, "tv", 28, "Madhouse", 9.3, ["adventure", "drama", "fantasy"]),
    ("Аптекарь", "The Apothecary Diaries", 2023, "tv", 24, "OLM", 8.8, ["drama", "mystery", "historical"]),
    ("Ранма 1/2", "Ranma 1/2", 2024, "tv", 12, "MAPPA", 8.0, ["action", "comedy", "romance"]),
    ("Моб Психо 100", "Mob Psycho 100", 2016, "tv", 37, "Bones", 8.7, ["action", "comedy", "supernatural"]),
    ("Мастера меча онлайн: Алисизация", "Sword Art Online: Alicization", 2018, "tv", 47, "A-1 Pictures", 7.6, ["action", "adventure", "fantasy", "isekai"]),
    ("Ванпанчмен 2", "One Punch Man 2", 2019, "tv", 12, "J.C.Staff", 7.4, ["action", "comedy", "supernatural"]),
    ("Токийский гуль: re", "Tokyo Ghoul: re", 2018, "tv", 24, "Pierrot", 6.8, ["action", "horror", "psychological"]),
    ("Яйцо ангела", "Angel's Egg", 1985, "movie", 1, "Studio Deen", 8.0, ["fantasy", "psychological", "supernatural"]),
    ("Идеальная грусть", "Perfect Blue", 1997, "movie", 1, "Madhouse", 8.5, ["psychological", "thriller"]),
    ("Красная черепаха", "The Red Turtle", 2016, "movie", 1, "Studio Ghibli", 8.0, ["adventure", "drama", "fantasy"]),
]


# ============ ГЕНЕРАЦИЯ ============
PREFIXES = [
    "Тайна", "Хроники", "Сага", "Легенда", "История", "Путь", "Мир",
    "Тени", "Свет", "Пламя", "Лёд", "Звёзды", "Небо", "Земля", "Ветер",
    "Кровь", "Сердце", "Душа", "Меч", "Щит", "Клинок", "Магия", "Сила",
    "Врата", "Королевство", "Империя", "Республика", "Город", "Деревня",
    "Академия", "Школа", "Клуб", "Отряд", "Команда", "Гильдия", "Орден",
    "Небесный", "Тёмный", "Светлый", "Вечный", "Последний", "Первый",
]

SUFFIXES = [
    "героев", "воинов", "магов", "демонов", "богов", "духов", "драконов",
    "самураев", "ниндзя", "пиратов", "рыцарей", "принцесс", "королей",
    "легенд", "мифов", "сказаний", "пророчеств", "судеб", "времён",
    "пространств", "измерений", "миров", "галактик", "вселенных",
    "академия", "школа", "гильдия", "орден", "храм", "дворец",
]

STUDIOS = [
    "MAPPA", "Madhouse", "Bones", "ufotable", "Production I.G",
    "A-1 Pictures", "Kyoto Animation", "Studio Ghibli", "Sunrise",
    "Pierrot", "White Fox", "Wit Studio", "J.C.Staff", "Studio Deen",
    "Silver Link", "Doga Kobo", "CloverWorks", "Science SARU", "8bit",
    "Kinema Citrus", "TMS Entertainment", "OLM", "Satelight", "Brain's Base",
]

ALL_GENRE_SLUGS = [g[1] for g in GENRES]


def generate_anime(count: int = 100) -> list[dict]:
    """Генерирует случайные аниме."""
    used_titles = set()
    result = []

    while len(result) < count:
        prefix = random.choice(PREFIXES)
        suffix = random.choice(SUFFIXES)
        title = f"{prefix} {suffix}"

        if title in used_titles:
            continue
        used_titles.add(title)

        year = random.randint(1995, 2025)
        anime_type = random.choice(["tv", "tv", "tv", "movie", "ova", "ona"])
        episodes = {
            "tv": random.randint(12, 200),
            "movie": 1,
            "ova": random.randint(1, 12),
            "ona": random.randint(1, 26),
        }[anime_type]
        studio = random.choice(STUDIOS)
        rating = round(random.uniform(6.5, 9.2), 1)
        rating_count = random.randint(100, 3000)
        genres = random.sample(ALL_GENRE_SLUGS, random.randint(2, 4))
        status = random.choice(["completed", "completed", "completed", "ongoing", "upcoming"])

        result.append({
            "title": title,
            "title_en": None,
            "title_jp": None,
            "description": (
                f"Захватывающая история о {prefix.lower()} {suffix}. "
                f"Герои сражаются, дружат и ищут своё место в мире."
            ),
            "year": year,
            "type": anime_type,
            "status": status,
            "episodes_total": episodes,
            "duration_minutes": random.choice([23, 24, 25]) if anime_type == "tv" else None,
            "studio": studio,
            "rating": rating,
            "rating_count": rating_count,
            "genres": genres,
        })

    return result


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
        else:
            print("Жанры уже есть")

        # Загружаем все жанры
        all_genres_result = await db.execute(select(Genre))
        genre_map = {g.slug: g for g in all_genres_result.scalars().all()}

        # 2. Существующие аниме
        existing_titles_result = await db.execute(select(Anime.title))
        existing_titles = {row[0] for row in existing_titles_result.all()}

        # 3. Реальные аниме
        added_real = 0
        for (title, title_en, year, anime_type, episodes, studio, rating, genres) in REAL_ANIME:
            if title in existing_titles:
                continue

            anime = Anime(
                title=title,
                title_en=title_en,
                year=year,
                type=AnimeType(anime_type),
                status=AnimeStatus.COMPLETED,
                episodes_total=episodes,
                duration_minutes=24 if anime_type == "tv" else None,
                studio=studio,
                rating=rating,
                rating_count=random.randint(500, 3000),
                description=f"Популярное аниме {title_en or title} ({year}).",
            )
            anime.genres = [genre_map[g] for g in genres if g in genre_map]
            db.add(anime)
            existing_titles.add(title)
            added_real += 1

        await db.flush()
        print(f"Добавлено реальных аниме: {added_real}")

        # 4. Сгенерированные аниме
        generated = generate_anime(count=100)
        added_gen = 0
        for data in generated:
            if data["title"] in existing_titles:
                continue

            genres = data.pop("genres")
            anime = Anime(**data)
            anime.genres = [genre_map[g] for g in genres if g in genre_map]
            db.add(anime)
            existing_titles.add(data["title"])
            added_gen += 1

        await db.commit()
        print(f"Добавлено сгенерированных аниме: {added_gen}")
        print(f"Всего добавлено: {added_real + added_gen}")
        print("Готово.")


if __name__ == "__main__":
    asyncio.run(seed())