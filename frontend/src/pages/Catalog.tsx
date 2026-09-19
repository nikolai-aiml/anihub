import { useState, type FormEvent } from "react";
import { useQuery } from "@tanstack/react-query";
import { animeApi } from "../api/anime";
import { AnimeCard } from "../components/AnimeCard";
import { Loader } from "../components/Loader";

export function Catalog() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [sort, setSort] = useState("rating");

  const { data, isLoading, error } = useQuery({
    queryKey: ["anime-list", page, search, sort],
    queryFn: () =>
      animeApi.list({ page, size: 20, search: search || undefined, sort }),
  });

  const handleSearch = (e: FormEvent) => {
    e.preventDefault();
    setPage(1);
    setSearch(searchInput);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Каталог аниме</h1>

      <div className="flex flex-col md:flex-row gap-4 mb-6">
        <form onSubmit={handleSearch} className="flex-1 flex gap-2">
          <input
            type="text"
            className="input"
            placeholder="Поиск по названию..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
          />
          <button type="submit" className="btn-primary">
            Найти
          </button>
        </form>

        <select
          className="input md:w-48"
          value={sort}
          onChange={(e) => {
            setSort(e.target.value);
            setPage(1);
          }}
        >
          <option value="rating">По рейтингу</option>
          <option value="year">По году</option>
          <option value="title">По названию</option>
        </select>
      </div>

      {isLoading && <Loader />}
      {error && (
        <div className="text-red-400 text-center py-12">Ошибка загрузки</div>
      )}

      {data && data.items.length === 0 && (
        <div className="text-center py-12 text-muted">Ничего не найдено</div>
      )}

      {data && data.items.length > 0 && (
        <>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {data.items.map((anime) => (
              <AnimeCard key={anime.id} anime={anime} />
            ))}
          </div>

          {data.pages > 1 && (
            <div className="flex justify-center items-center gap-4 mt-8">
              <button
                disabled={page === 1}
                onClick={() => setPage((p) => p - 1)}
                className="btn-ghost"
              >
                Назад
              </button>
              <span className="text-sm text-muted">
                Страница {data.page} из {data.pages}
              </span>
              <button
                disabled={page === data.pages}
                onClick={() => setPage((p) => p + 1)}
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