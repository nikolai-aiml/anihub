"""Поиск постеров через AniList API по русскому названию."""

import asyncio

import httpx


# Русское название → поисковый запрос на AniList
ANIME_LIST = {
    "Берсерк": "Berserk",
    "Могила светлячков": "Hotaru no Haka",
    "Токийские мстители": "Tokyo Revengers",
    "Акира": "Akira",
    "Идеальная грусть": "Perfect Blue",
    "Гуррен-Лаганн": "Tengen Toppa Gurren Lagann",
    "Бездомный бог": "Noragami",
    "О моём перерождении в слизь": "Tensei Shitara Slime Datta Ken",
    "Королевство": "Kingdom",
    "Дорохедоро": "Dorohedoro",
    "Магическая битва 2": "Jujutsu Kaisen 2nd Season",
    "Кайдзю №8": "Kaijuu 8-gou",
    "Дандадан": "Dandadan",
    "Соло Левелинг": "Ore dake Level Up na Ken",
    "Аптекарь": "Kusuriya no Hitorigoto",
    "Сага о Винланде 2": "Vinland Saga Season 2",
    "Токийские мстители: Сезон 3": "Tokyo Revengers: Tenjiku-hen",
    "Тетрадь дружбы Нацумэ 7": "Natsume Yuujinchou Shichi",
    "Магическая битва 0": "Jujutsu Kaisen 0 Movie",
}


QUERY = """
query ($search: String) {
  Media(search: $search, type: ANIME, sort: SEARCH_MATCH) {
    id
    title { romaji english native }
    coverImage { extraLarge large }
  }
}
"""


async def find():
    results = {}
    async with httpx.AsyncClient(timeout=20) as client:
        for ru_title, search in ANIME_LIST.items():
            try:
                r = await client.post(
                    "https://graphql.anilist.co",
                    json={"query": QUERY, "variables": {"search": search}},
                )
                if r.status_code == 200:
                    data = r.json()
                    media = data.get("data", {}).get("Media")
                    if media:
                        cover = media["coverImage"]["extraLarge"] or media["coverImage"]["large"]
                        romaji = media["title"]["romaji"]
                        print(f'    "{ru_title}": "{cover}",  # {romaji}')
                        results[ru_title] = cover
                    else:
                        print(f'    # НЕ НАЙДЕНО: {ru_title} ({search})')
                else:
                    print(f'    # ОШИБКА {r.status_code}: {ru_title}')
            except Exception as e:
                print(f'    # ИСКЛЮЧЕНИЕ: {ru_title} → {e}')

    print("\n\n=== ГОТОВЫЙ СЛОВАРЬ ===\n")
    print("FIXES = {")
    for title, url in results.items():
        print(f'    "{title}": "{url}",')
    print("}")


if __name__ == "__main__":
    asyncio.run(find())