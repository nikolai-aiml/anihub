import {
  RARITY_COLORS,
  RARITY_LABELS,
  type UserAchievement,
} from "../types";
import { LockIcon } from "./icons";

interface AchievementCardProps {
  achievement: UserAchievement;
}

export function AchievementCard({ achievement }: AchievementCardProps) {
  const { icon, title, description, rarity, target, progress, is_unlocked, unlocked_at } = achievement;

  const percentage = target > 0 ? (progress / target) * 100 : 0;
  const rarityColor = RARITY_COLORS[rarity];

  const unlockedDate = unlocked_at
    ? new Date(unlocked_at).toLocaleDateString("ru-RU", {
        day: "numeric",
        month: "short",
        year: "numeric",
      })
    : null;

  return (
    <div
      className={`
        relative glass rounded-2xl p-5 border transition-all duration-300
        ${is_unlocked ? `${rarityColor} hover:scale-[1.02] hover:shadow-2xl` : "border-white/5 opacity-70"}
      `}
    >
      {/* Редкость (бейдж) */}
      <div className="flex items-start justify-between mb-4">
        <div
          className={`
            w-14 h-14 rounded-2xl flex items-center justify-center text-3xl
            ${is_unlocked ? "bg-white/5" : "bg-black/30 grayscale"}
          `}
        >
          {is_unlocked ? icon : <LockIcon className="w-6 h-6 text-gray-500" />}
        </div>

        <span
          className={`
            text-xs px-2 py-1 rounded-lg border font-medium uppercase tracking-wider
            ${rarityColor}
          `}
        >
          {RARITY_LABELS[rarity]}
        </span>
      </div>

      {/* Название и описание */}
      <h3 className="text-lg font-bold font-display mb-1">{title}</h3>
      <p className="text-sm text-gray-400 mb-4 leading-relaxed">{description}</p>

      {/* Прогресс */}
      {!is_unlocked ? (
        <>
          <div className="flex items-center justify-between text-xs text-muted mb-2">
            <span>Прогресс</span>
            <span className="tabular-nums font-medium">
              {progress} / {target}
            </span>
          </div>
          <div className="h-2 bg-white/5 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-primary to-accent rounded-full transition-all duration-700"
              style={{ width: `${Math.min(percentage, 100)}%` }}
            />
          </div>
        </>
      ) : (
        <div className="flex items-center gap-2 text-xs text-muted">
          <span>✓ Получено</span>
          {unlockedDate && <span>· {unlockedDate}</span>}
        </div>
      )}
    </div>
  );
}