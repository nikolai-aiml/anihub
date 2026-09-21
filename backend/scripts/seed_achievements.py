"""Seed достижений."""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.achievement import (
    Achievement,
    AchievementCategory,
    AchievementRarity,
)


ACHIEVEMENTS = [
    {
        "code": "first_step",
        "title": "First Step",
        "description": "Добавьте первое аниме в библиотеку",
        "icon": "🌟",
        "rarity": AchievementRarity.COMMON,
        "category": AchievementCategory.LIBRARY,
        "target": 1,
    },
    {
        "code": "collector_10",
        "title": "Collector",
        "description": "Добавьте 10 аниме в библиотеку",
        "icon": "📚",
        "rarity": AchievementRarity.COMMON,
        "category": AchievementCategory.LIBRARY,
        "target": 10,
    },
    {
        "code": "collector_50",
        "title": "True Collector",
        "description": "Добавьте 50 аниме в библиотеку",
        "icon": "📖",
        "rarity": AchievementRarity.RARE,
        "category": AchievementCategory.LIBRARY,
        "target": 50,
    },
    {
        "code": "critic_1",
        "title": "First Rating",
        "description": "Поставьте первую оценку",
        "icon": "⭐",
        "rarity": AchievementRarity.COMMON,
        "category": AchievementCategory.RATINGS,
        "target": 1,
    },
    {
        "code": "critic_10",
        "title": "Critic",
        "description": "Поставьте 10 оценок",
        "icon": "✨",
        "rarity": AchievementRarity.COMMON,
        "category": AchievementCategory.RATINGS,
        "target": 10,
    },
    {
        "code": "critic_50",
        "title": "Master Critic",
        "description": "Поставьте 50 оценок",
        "icon": "💫",
        "rarity": AchievementRarity.RARE,
        "category": AchievementCategory.RATINGS,
        "target": 50,
    },
    {
        "code": "reviewer_1",
        "title": "First Review",
        "description": "Напишите первый отзыв",
        "icon": "✍️",
        "rarity": AchievementRarity.COMMON,
        "category": AchievementCategory.REVIEWS,
        "target": 1,
    },
    {
        "code": "reviewer_10",
        "title": "Reviewer",
        "description": "Напишите 10 отзывов",
        "icon": "📝",
        "rarity": AchievementRarity.RARE,
        "category": AchievementCategory.REVIEWS,
        "target": 10,
    },
    {
        "code": "favorites_10",
        "title": "Curator",
        "description": "Добавьте 10 аниме в избранное",
        "icon": "❤️",
        "rarity": AchievementRarity.COMMON,
        "category": AchievementCategory.FAVORITES,
        "target": 10,
    },
    {
        "code": "favorites_25",
        "title": "Favorites Master",
        "description": "Добавьте 25 аниме в избранное",
        "icon": "💖",
        "rarity": AchievementRarity.EPIC,
        "category": AchievementCategory.FAVORITES,
        "target": 25,
    },
    {
        "code": "veteran_30",
        "title": "Veteran",
        "description": "Используйте ANIHUB 30 дней",
        "icon": "🎖️",
        "rarity": AchievementRarity.LEGENDARY,
        "category": AchievementCategory.SPECIAL,
        "target": 30,
    },
    {
        "code": "all_rounder",
        "title": "All-Rounder",
        "description": "10+ в каждой категории",
        "icon": "🏆",
        "rarity": AchievementRarity.EPIC,
        "category": AchievementCategory.SPECIAL,
        "target": 10,
    },
]


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(Achievement.code))
        existing_codes = {row[0] for row in existing.all()}

        added = 0
        for data in ACHIEVEMENTS:
            if data["code"] in existing_codes:
                continue
            db.add(Achievement(**data))
            added += 1

        await db.commit()
        print(f"Добавлено достижений: {added}")
        print("Готово.")


if __name__ == "__main__":
    asyncio.run(seed())