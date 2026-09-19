import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { animeApi } from "../api/anime";
import { Loader } from "../components/Loader";

export function Anime() {
  const { id } = useParams<{ id: string }>();
  const animeId = Number(id);

  const { data: anime, isLoading, error } = useQuery({
    queryKey: ["anime", animeId],
    queryFn: () => animeApi.getById(animeId),
    enabled: !isNaN(animeId),
  });

  if (isLoading) return <Loader />;

  if (error || !anime) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <p className="text-muted mb-4">Аниме не найдено</p>
        <Link to="/catalog" className="btn-primary inline-block">
          Вернуться в каталог
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Link to="/catalog" className="text-sm text-muted hover:text-white">
        ← Назад в каталог
      </Link>

      <div className="grid grid-cols-1 md:grid-cols-[300px_1fr] gap-8 mt-6">
        <div className="aspect-[2/3] bg-surface rounded-xl overflow-hidden border border-border">
          {anime.poster_url ? (
            <img
              src={anime.poster_url}
              alt={anime.title}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-6xl">
              🎬
            </div>
          )}
        </div>

        <div>
          <h1 className="text-4xl font-bold">{anime.title}</h1>
          {anime.title_en && <p className="text-muted mt-1">{anime.title_en}</p>}
          {anime.title_jp && (
            <p className="text-muted text-sm">{anime.title_jp}</p>
          )}

          <div className="flex flex-wrap items-center gap-4 mt-4 text-sm">
            <span className="bg-primary/20 text-primary px-3 py-1 rounded-full font-bold">
              ⭐ {anime.rating.toFixed(1)}
            </span>
            <span className="text-muted">{anime.rating_count} оценок</span>
            {anime.year && <span className="text-muted">{anime.year}</span>}
            <span className="text-muted uppercase">{anime.type}</span>
            <span className="text-muted">{anime.status}</span>
          </div>

          <div className="flex flex-wrap gap-2 mt-4">
            {anime.genres.map((g) => (
              <span
                key={g.id}
                className="bg-surface border border-border px-3 py-1 rounded-full text-sm"
              >
                {g.name}
              </span>
            ))}
          </div>

          {anime.description && (
            <p className="mt-6 leading-relaxed text-gray-300">
              {anime.description}
            </p>
          )}

          <div className="grid grid-cols-2 gap-4 mt-6 text-sm">
            {anime.studio && (
              <div>
                <span className="text-muted">Студия:</span> {anime.studio}
              </div>
            )}
            {anime.episodes_total && (
              <div>
                <span className="text-muted">Эпизодов:</span>{" "}
                {anime.episodes_total}
              </div>
            )}
            {anime.duration_minutes && (
              <div>
                <span className="text-muted">Длительность:</span>{" "}
                {anime.duration_minutes} мин
              </div>
            )}
          </div>

          <button className="btn-primary mt-8">Добавить в библиотеку</button>
        </div>
      </div>
    </div>
  );
}