import { Link } from "react-router-dom";
import type { AnimeListItem } from "../types";

export function AnimeCard({ anime }: { anime: AnimeListItem }) {
  return (
    <Link
      to={`/anime/${anime.id}`}
      className="card hover:border-primary transition-colors group"
    >
      <div className="aspect-[2/3] bg-bg relative overflow-hidden">
        {anime.poster_url ? (
          <img
            src={anime.poster_url}
            alt={anime.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-muted text-6xl">
            🎬
          </div>
        )}
        <div className="absolute top-2 right-2 bg-black/70 backdrop-blur px-2 py-1 rounded text-sm font-bold">
          ⭐ {anime.rating.toFixed(1)}
        </div>
      </div>
      <div className="p-3">
        <h3 className="font-semibold line-clamp-2 min-h-[2.5rem]">
          {anime.title}
        </h3>
        <div className="flex items-center gap-2 mt-2 text-xs text-muted">
          <span>{anime.year || "—"}</span>
          <span>•</span>
          <span className="uppercase">{anime.type}</span>
        </div>
      </div>
    </Link>
  );
}