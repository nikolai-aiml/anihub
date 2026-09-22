import type { GenreCount } from "../../types";

interface TopGenresProps {
  genres: GenreCount[];
}

export function TopGenres({ genres }: TopGenresProps) {
  if (genres.length === 0) {
    return (
      <div className="glass rounded-2xl p-6 border border-white/5">
        <h3 className="text-lg font-bold font-display mb-4">Любимые жанры</h3>
        <p className="text-muted text-sm text-center py-8">
          Добавь аниме в библиотеку, чтобы увидеть статистику жанров
        </p>
      </div>
    );
  }

  const maxCount = Math.max(...genres.map((g) => g.count), 1);

  return (
    <div className="glass rounded-2xl p-6 border border-white/5">
      <h3 className="text-lg font-bold font-display mb-6">Любимые жанры</h3>

      <div className="space-y-3">
        {genres.map((genre, index) => {
          const percentage = (genre.count / maxCount) * 100;
          const colors = [
            "from-blue-500 to-cyan-500",
            "from-purple-500 to-pink-500",
            "from-yellow-500 to-orange-500",
            "from-green-500 to-emerald-500",
            "from-red-500 to-rose-500",
          ];
          const color = colors[index % colors.length];

          return (
            <div key={genre.genre} className="flex items-center gap-3">
              <div className="w-24 text-sm text-white font-medium truncate">
                {genre.genre}
              </div>

              <div className="flex-1 h-7 bg-white/5 rounded-lg overflow-hidden">
                <div
                  className={`h-full bg-gradient-to-r ${color} rounded-lg transition-all duration-700`}
                  style={{ width: `${percentage}%` }}
                />
              </div>

              <div className="w-12 text-right text-sm tabular-nums text-muted">
                {genre.count}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}