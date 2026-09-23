import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRightIcon } from "./icons";
import type { AnimeListItem } from "../types";

interface SpotlightCarouselProps {
  label: string;
  subtitle?: string;
  anime: AnimeListItem[];
  autoPlayInterval?: number;
}

export function SpotlightCarousel({
  label,
  subtitle,
  anime,
  autoPlayInterval = 4000,
}: SpotlightCarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (anime.length <= 1) return;

    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % anime.length);
    }, autoPlayInterval);

    return () => clearInterval(interval);
  }, [anime.length, autoPlayInterval]);

  if (anime.length === 0) return null;

  const current = anime[currentIndex];

  return (
    <div className="glass rounded-3xl overflow-hidden border border-white/10 relative">
      <div className="relative aspect-[16/9] md:aspect-[21/9]">
        {/* BLURRED BACKGROUND */}
        <AnimatePresence mode="wait">
          <motion.div
            key={`bg-${current.id}`}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.8 }}
            className="absolute inset-0"
          >
            {current.poster_url ? (
              <img
                src={current.poster_url}
                alt=""
                className="w-full h-full object-cover scale-110 blur-2xl brightness-50"
                referrerPolicy="no-referrer"
                onError={(e) => {
                  (e.target as HTMLImageElement).style.display = "none";
                }}
              />
            ) : (
              <div className="w-full h-full bg-gradient-to-br from-primary/70 via-purple-700/50 to-accent/70" />
            )}
          </motion.div>
        </AnimatePresence>

        {/* Тёмный оверлей */}
        <div className="absolute inset-0 bg-gradient-to-r from-black/95 via-black/80 to-black/40" />

        {/* КОНТЕНТ */}
        <div className="absolute inset-0 flex items-center">
          <div className="flex flex-col md:flex-row items-center md:items-stretch gap-6 md:gap-10 p-6 md:p-10 w-full">
            {/* ПОСТЕР (чёткий, вертикальный) */}
            <AnimatePresence mode="wait">
              <motion.div
                key={`poster-${current.id}`}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
                className="flex-shrink-0 w-32 md:w-48 lg:w-56 aspect-[2/3] rounded-2xl overflow-hidden shadow-2xl border border-white/10"
              >
                {current.poster_url ? (
                  <img
                    src={current.poster_url}
                    alt={current.title}
                    className="w-full h-full object-cover"
                    referrerPolicy="no-referrer"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.display = "none";
                      if (target.parentElement) {
                        target.parentElement.innerHTML =
                          '<div class="w-full h-full bg-gradient-to-br from-primary/60 to-accent/60 flex items-center justify-center text-4xl">🎬</div>';
                      }
                    }}
                  />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-primary/60 to-accent/60 flex items-center justify-center text-4xl">
                    🎬
                  </div>
                )}
              </motion.div>
            </AnimatePresence>

            {/* ТЕКСТ */}
            <AnimatePresence mode="wait">
              <motion.div
                key={`info-${current.id}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
                className="flex-1 min-w-0 flex flex-col justify-center"
              >
                {/* Метка */}
                <div className="mb-3">
                  <span className="text-xs uppercase tracking-widest text-primary font-bold">
                    {label}
                  </span>
                  {subtitle && (
                    <p className="text-xs text-gray-400 mt-1">{subtitle}</p>
                  )}
                </div>

                {/* Название */}
                <h3 className="text-2xl md:text-4xl lg:text-5xl font-bold font-display text-white mb-4 line-clamp-2">
                  {current.title}
                </h3>

                {/* Мета */}
                <div className="flex flex-wrap items-center gap-3 text-sm text-gray-300 mb-5">
                  <span className="flex items-center gap-1 bg-yellow-500/10 border border-yellow-500/30 px-2 py-0.5 rounded-lg text-yellow-400 font-bold">
                    ★ {current.rating.toFixed(1)}
                  </span>
                  {current.year && <span>• {current.year}</span>}
                  <span className="uppercase">• {current.type}</span>
                  {current.episodes_total && (
                    <span>• {current.episodes_total} эп.</span>
                  )}
                </div>

                {/* Жанры */}
                {current.genres.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-5">
                    {current.genres.slice(0, 4).map((g) => (
                      <span
                        key={g.id}
                        className="text-xs px-2.5 py-1 rounded-full bg-white/5 border border-white/10 text-gray-300"
                      >
                        {g.name}
                      </span>
                    ))}
                  </div>
                )}

                {/* Кнопка */}
                <Link
                  to={`/anime/${current.id}`}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary hover:bg-primary-hover text-white font-medium transition-all duration-300 hover:scale-105 active:scale-95 w-fit"
                >
                  Смотреть
                  <ArrowRightIcon className="w-4 h-4" />
                </Link>
              </motion.div>
            </AnimatePresence>
          </div>
        </div>

        {/* Индикаторы */}
        {anime.length > 1 && (
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-1.5 z-10">
            {anime.map((_, i) => (
              <button
                key={i}
                onClick={() => setCurrentIndex(i)}
                className={`
                  h-1.5 rounded-full transition-all duration-300
                  ${
                    i === currentIndex
                      ? "w-8 bg-primary"
                      : "w-1.5 bg-white/30 hover:bg-white/50"
                  }
                `}
                aria-label={`Слайд ${i + 1}`}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}