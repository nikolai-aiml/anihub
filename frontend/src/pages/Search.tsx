import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { animeApi } from "../api/anime";
import { AnimeCard } from "../components/AnimeCard";
import { AnimeGridSkeleton } from "../components/AnimeCardSkeleton";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { SearchIcon, CompassIcon } from "../components/icons";

export function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [input, setInput] = useState(searchParams.get("q") || "");

  const query = searchParams.get("q") || "";
  const sort = searchParams.get("sort") || "rating";
  const page = Number(searchParams.get("page") || "1");

  // Debounce ввода
  useEffect(() => {
    const timer = setTimeout(() => {
      if (input.trim() && input !== query) {
        setSearchParams({ q: input, sort, page: "1" });
      } else if (!input.trim() && query) {
        setSearchParams({ sort, page: "1" });
      }
    }, 400);

    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [input]);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["search", query, sort, page],
    queryFn: () =>
      animeApi.list({
        search: query || undefined,
        sort,
        page,
        size: 20,
      }),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSearchParams({ q: input, sort, page: "1" });
  };

  return (
    <div className="container mx-auto px-6 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-display mb-6">Поиск</h1>

        {/* Большое поле поиска */}
        <form onSubmit={handleSubmit} className="relative">
          <div className="relative">
            <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted pointer-events-none" />
            <input
              type="text"
              className="input pl-12 py-4 text-lg"
              placeholder="Найти аниме..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              autoFocus
            />
          </div>
        </form>
      </div>

      {/* Фильтры */}
      {query && (
        <div className="flex flex-wrap items-center gap-3 mb-6">
          <span className="text-sm text-muted">Сортировка:</span>
          {[
            { value: "rating", label: "По рейтингу" },
            { value: "year", label: "По году" },
            { value: "title", label: "По названию" },
          ].map((s) => (
            <button
              key={s.value}
              onClick={() => setSearchParams({ q: query, sort: s.value, page: "1" })}
              className={`
                px-3 py-1.5 rounded-lg text-sm transition-all
                ${
                  sort === s.value
                    ? "bg-primary/20 text-primary border border-primary/40"
                    : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
                }
              `}
            >
              {s.label}
            </button>
          ))}
        </div>
      )}

      {/* Ничего не введено */}
      {!query && (
        <EmptyState
          icon={<SearchIcon className="w-10 h-10" />}
          title="Начни поиск"
          description="Введи название аниме, чтобы найти его в каталоге"
          actionLabel="Открыть каталог"
          actionTo="/catalog"
        />
      )}

      {/* Загрузка */}
      {query && isLoading && <AnimeGridSkeleton count={10} />}

      {/* Ошибка */}
      {query && error && (
        <ErrorState
          title="Не удалось выполнить поиск"
          description="Проверьте соединение и попробуйте снова"
          onRetry={() => refetch()}
        />
      )}

      {/* Пусто */}
      {query && data && data.items.length === 0 && (
        <EmptyState
          icon={<CompassIcon className="w-10 h-10" />}
          title="Ничего не найдено"
          description={`По запросу «${query}» ничего не нашлось. Попробуй другое название.`}
          actionLabel="Вернуться в каталог"
          actionTo="/catalog"
        />
      )}

      {/* Результаты */}
      {query && data && data.items.length > 0 && (
        <>
          <div className="text-sm text-muted mb-4">
            Найдено: <span className="text-white font-medium">{data.total}</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {data.items.map((anime) => (
              <AnimeCard key={anime.id} anime={anime} />
            ))}
          </div>

          {data.pages > 1 && (
            <div className="flex justify-center items-center gap-4 mt-8">
              <button
                disabled={page === 1}
                onClick={() =>
                  setSearchParams({ q: query, sort, page: String(page - 1) })
                }
                className="btn-ghost"
              >
                Назад
              </button>
              <span className="text-sm text-muted">
                Страница {data.page} из {data.pages}
              </span>
              <button
                disabled={page === data.pages}
                onClick={() =>
                  setSearchParams({ q: query, sort, page: String(page + 1) })
                }
                className="btn-ghost"
              >
                Вперёд
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}