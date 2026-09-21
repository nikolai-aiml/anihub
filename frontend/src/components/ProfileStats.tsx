import { Link } from "react-router-dom";
import { BookIcon, HeartIcon, StarIcon, EditIcon } from "./icons";
import type { ProfileStats as Stats } from "../types";

interface ProfileStatsProps {
  stats: Stats;
}

const items = [
  {
    key: "library_total",
    label: "Аниме в библиотеке",
    shortLabel: "Аниме",
    icon: BookIcon,
    to: "/library",
    color: "text-blue-400 bg-blue-500/10 border-blue-500/30",
  },
  {
    key: "ratings_total",
    label: "Оценок",
    shortLabel: "Оценок",
    icon: StarIcon,
    to: "/statistics",
    color: "text-yellow-400 bg-yellow-500/10 border-yellow-500/30",
  },
  {
    key: "reviews_total",
    label: "Отзывов",
    shortLabel: "Отзывов",
    icon: EditIcon,
    to: "/statistics",
    color: "text-purple-400 bg-purple-500/10 border-purple-500/30",
  },
  {
    key: "favorites_total",
    label: "В избранном",
    shortLabel: "Избранное",
    icon: HeartIcon,
    to: "/favorites",
    color: "text-pink-400 bg-pink-500/10 border-pink-500/30",
  },
] as const;

export function ProfileStats({ stats }: ProfileStatsProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {items.map((item) => {
        const Icon = item.icon;
        const value = stats[item.key];

        return (
          <Link
            key={item.key}
            to={item.to}
            className={`
              glass rounded-2xl p-5 border ${item.color}
              hover:scale-[1.02] hover:shadow-2xl transition-all duration-300
              group
            `}
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center">
                <Icon className="w-5 h-5" />
              </div>
              <span className="text-xs uppercase tracking-wider opacity-60">
                {item.shortLabel}
              </span>
            </div>
            <div className="text-3xl font-bold font-display tabular-nums">
              {value}
            </div>
            <div className="text-xs text-muted mt-1">{item.label}</div>
          </Link>
        );
      })}
    </div>
  );
}