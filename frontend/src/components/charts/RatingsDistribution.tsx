interface RatingsDistributionProps {
  distribution: Record<string, number>;
}

export function RatingsDistribution({ distribution }: RatingsDistributionProps) {
  const ratings = Array.from({ length: 10 }, (_, i) => String(10 - i));
  const maxCount = Math.max(...Object.values(distribution), 1);

  return (
    <div className="glass rounded-2xl p-6 border border-white/5">
      <h3 className="text-lg font-bold font-display mb-6">
        Распределение оценок
      </h3>

      <div className="space-y-3">
        {ratings.map((rating) => {
          const count = distribution[rating] || 0;
          const percentage = (count / maxCount) * 100;

          return (
            <div key={rating} className="flex items-center gap-3">
              <div className="flex items-center gap-1 w-14 text-sm text-muted">
                <span className="font-bold text-white">{rating}</span>
                <span>★</span>
              </div>

              <div className="flex-1 h-7 bg-white/5 rounded-lg overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-primary to-accent rounded-lg transition-all duration-700"
                  style={{ width: `${percentage}%` }}
                />
              </div>

              <div className="w-12 text-right text-sm tabular-nums text-muted">
                {count}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}