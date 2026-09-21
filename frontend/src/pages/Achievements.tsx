import { useState, useMemo } from "react";
import { useAchievements } from "../hooks/useAchievements";
import { AchievementCard } from "../components/AchievementCard";
import { Loader } from "../components/Loader";
import { TrophyIcon } from "../components/icons";

type Filter = "all" | "unlocked" | "locked";

export function Achievements() {
  const { data: achievements = [], isLoading } = useAchievements();
  const [filter, setFilter] = useState<Filter>("all");

  const stats = useMemo(() => {
    const total = achievements.length;
    const unlocked = achievements.filter((a) => a.is_unlocked).length;
    return { total, unlocked };
  }, [achievements]);

  const filtered = useMemo(() => {
    if (filter === "unlocked") return achievements.filter((a) => a.is_unlocked);
    if (filter === "locked") return achievements.filter((a) => !a.is_unlocked);
    return achievements;
  }, [achievements, filter]);

  if (isLoading) return <Loader />;

  const TABS: Array<{ value: Filter; label: string; count: number }> = [
    { value: "all", label: "Все", count: stats.total },
    { value: "unlocked", label: "Полученные", count: stats.unlocked },
    { value: "locked", label: "В процессе", count: stats.total - stats.unlocked },
  ];

  return (
    <div className="container mx-auto px-6 py-8">
      {/* Заголовок */}
      <div className="flex items-center gap-4 mb-8">
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg shadow-primary/30">
          <TrophyIcon className="w-7 h-7 text-white" />
        </div>
        <div>
          <h1 className="text-3xl font-bold font-display">Достижения</h1>
          <p className="text-muted text-sm mt-1">
            {stats.unlocked} из {stats.total} получено
          </p>
        </div>
      </div>

      {/* Общий прогресс */}
      <div className="glass rounded-2xl p-5 border border-white/5 mb-8">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm text-gray-300">Общий прогресс</span>
          <span className="text-sm font-bold tabular-nums">
            {stats.total > 0
              ? Math.round((stats.unlocked / stats.total) * 100)
              : 0}
            %
          </span>
        </div>
        <div className="h-3 bg-white/5 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-primary via-accent to-primary bg-[length:200%_100%] animate-gradient-shift rounded-full transition-all duration-700"
            style={{
              width: `${
                stats.total > 0 ? (stats.unlocked / stats.total) * 100 : 0
              }%`,
            }}
          />
        </div>
      </div>

      {/* Табы */}
      <div className="flex flex-wrap gap-2 mb-6">
        {TABS.map((tab) => (
          <button
            key={tab.value}
            onClick={() => setFilter(tab.value)}
            className={`
              px-4 py-2 rounded-xl text-sm font-medium transition-all flex items-center gap-2
              ${
                filter === tab.value
                  ? "bg-primary/20 text-primary border border-primary/40"
                  : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
              }
            `}
          >
            {tab.label}
            <span
              className={`
                text-xs px-1.5 py-0.5 rounded-md
                ${filter === tab.value ? "bg-primary/30" : "bg-white/10"}
              `}
            >
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* Пусто */}
      {filtered.length === 0 && (
        <div className="text-center py-20">
          <p className="text-muted">
            {filter === "unlocked"
              ? "Пока нет полученных достижений"
              : filter === "locked"
              ? "Все достижения получены! 🎉"
              : "Нет достижений"}
          </p>
        </div>
      )}

      {/* Сетка */}
      {filtered.length > 0 && (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((achievement) => (
            <AchievementCard
              key={achievement.id}
              achievement={achievement}
            />
          ))}
        </div>
      )}
    </div>
  );
}