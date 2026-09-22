import { useStatistics } from "../hooks/useStatistics";
import { Loader } from "../components/Loader";
import { RatingsDistribution } from "../components/charts/RatingsDistribution";
import { TopGenres } from "../components/charts/TopGenres";
import { ActivityChart } from "../components/charts/ActivityChart";
import { StarIcon, BookIcon, HeartIcon } from "../components/icons";

export function Statistics() {
  const { data: stats, isLoading } = useStatistics();

  if (isLoading) return <Loader />;
  if (!stats) return null;

  const { summary } = stats;

  const summaryCards = [
    {
      label: "Средняя оценка",
      value: summary.average_rating.toFixed(1),
      icon: StarIcon,
      color: "text-yellow-400 bg-yellow-500/10 border-yellow-500/30",
    },
    {
      label: "Всего оценок",
      value: summary.total_ratings,
      icon: StarIcon,
      color: "text-purple-400 bg-purple-500/10 border-purple-500/30",
    },
    {
      label: "Аниме в библиотеке",
      value: summary.library_total,
      icon: BookIcon,
      color: "text-blue-400 bg-blue-500/10 border-blue-500/30",
    },
    {
      label: "Избранное",
      value: summary.favorites_total,
      icon: HeartIcon,
      color: "text-pink-400 bg-pink-500/10 border-pink-500/30",
    },
  ];

  return (
    <div className="container mx-auto px-6 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-display">Статистика</h1>
        <p className="text-muted text-sm mt-1">
          Твоя активность и предпочтения
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {summaryCards.map((card) => {
          const Icon = card.icon;
          return (
            <div
              key={card.label}
              className={`glass rounded-2xl p-5 border ${card.color}`}
            >
              <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center mb-3">
                <Icon className="w-5 h-5" />
              </div>
              <div className="text-3xl font-bold font-display tabular-nums">
                {card.value}
              </div>
              <div className="text-xs text-muted mt-1">{card.label}</div>
            </div>
          );
        })}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <RatingsDistribution distribution={stats.ratings_distribution} />
        <TopGenres genres={stats.top_genres} />
      </div>

      <div className="mt-6">
        <ActivityChart activity={stats.activity_by_month} />
      </div>
    </div>
  );
}