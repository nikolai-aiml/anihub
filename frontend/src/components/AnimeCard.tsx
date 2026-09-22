import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import type { AnimeListItem } from "../types";

export function AnimeCard({ anime }: { anime: AnimeListItem }) {
  return (
    <motion.div
      whileHover={{ y: -8, scale: 1.03 }}
      whileTap={{ scale: 0.98 }}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
    >
      <Link
        to={`/anime/${anime.id}`}
        className="group block relative overflow-hidden rounded-2xl bg-surface border border-border hover:border-primary/50 transition-all duration-500 hover:shadow-2xl hover:shadow-primary/20"
      >
        <div className="aspect-[2/3] bg-bg relative overflow-hidden">
          {anime.poster_url ? (
            <img
              src={anime.poster_url}
              alt={anime.title}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-muted text-6xl">
              🎬
            </div>
          )}

          {/* Градиент снизу */}
          <div className="absolute inset-0 bg-gradient-to-t from-black via-black/30 to-transparent opacity-80" />

          {/* Рейтинг */}
          <div className="absolute top-3 right-3 bg-black/80 backdrop-blur-md px-2.5 py-1 rounded-lg text-sm font-bold flex items-center gap-1">
            <span className="text-yellow-400">★</span>
            {anime.rating.toFixed(1)}
          </div>

          {/* Текст поверх постера */}
          <div className="absolute bottom-0 left-0 right-0 p-4">
            <h3 className="font-bold text-white line-clamp-2 text-base leading-tight">
              {anime.title}
            </h3>
            <div className="flex items-center gap-2 mt-2 text-xs text-gray-400">
              {anime.year && <span>{anime.year}</span>}
              <span>•</span>
              <span className="uppercase">{anime.type}</span>
              {anime.episodes_total && (
                <>
                  <span>•</span>
                  <span>{anime.episodes_total} эп.</span>
                </>
              )}
            </div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}