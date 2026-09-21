import { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { useLibrary } from "../hooks/useLibrary";
import { AnimeCard } from "../components/AnimeCard";
import { Loader } from "../components/Loader";
import { BookIcon, ArrowRightIcon } from "../components/icons";
import { LIBRARY_STATUS_LABELS, type LibraryStatus } from "../types";

const TABS: Array<{ value: LibraryStatus | "all"; label: string }> = [
  { value: "all", label: "Все" },
  { value: "watching", label: "Смотрю" },
  { value: "planned", label: "Буду смотреть" },
  { value: "completed", label: "Завершено" },
  { value: "on_hold", label: "Отложено" },
  { value: "dropped", label: "Брошено" },
];

export function Library() {
  const [activeTab, setActiveTab] = useState<LibraryStatus | "all">("all");
  const { data: allEntries = [], isLoading } = useLibrary();

  // Фильтрация на клиенте
  const entries = useMemo(() => {
    if (activeTab === "all") return allEntries;
    return allEntries.filter((e) => e.status === activeTab);
  }, [allEntries, activeTab]);

  // Счётчики для каждого таба
  const counts = useMemo(() => {
    const result: Record<string, number> = { all: allEntries.length };
    allEntries.forEach((e) => {
      result[e.status] = (result[e.status] || 0) + 1;
    });
    return result;
  }, [allEntries]);

  if (isLoading) return <Loader />;

  // Empty state — библиотека пуста целиком
  if (allEntries.length === 0) {
    return (
      <div className="container mx-auto px-6 py-20 text-center">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-primary/10 border border-primary/20 mb-6">
          <BookIcon className="w-10 h-10 text-primary" />
        </div>
        <h1 className="text-3xl font-bold font-display mb-3">
          Библиотека пуста
        </h1>
        <p className="text-muted max-w-md mx-auto mb-8">
          Добавь первое аниме и начни собирать свою коллекцию.
        </p>
        <Link
          to="/catalog"
          className="btn-primary inline-flex items-center gap-2"
        >
          Открыть каталог
          <ArrowRightIcon className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-6 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-display">Моя библиотека</h1>
        <p className="text-muted text-sm mt-1">
          {allEntries.length} {allEntries.length === 1 ? "аниме" : "аниме"}
        </p>
      </div>

      {/* Табы со счётчиками */}
      <div className="flex flex-wrap gap-2 mb-8">
        {TABS.map((tab) => {
          const count = counts[tab.value] || 0;
          const isActive = activeTab === tab.value;
          return (
            <button
              key={tab.value}
              onClick={() => setActiveTab(tab.value)}
              className={`
                px-4 py-2 rounded-xl text-sm font-medium transition-all
                flex items-center gap-2
                ${
                  isActive
                    ? "bg-primary/20 text-primary border border-primary/40"
                    : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
                }
              `}
            >
              {tab.label}
              {count > 0 && (
                <span
                  className={`
                    text-xs px-1.5 py-0.5 rounded-md
                    ${isActive ? "bg-primary/30" : "bg-white/10"}
                  `}
                >
                  {count}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Пусто в этом табе */}
      {entries.length === 0 && (
        <div className="text-center py-20">
          <p className="text-muted">
            В категории «{LIBRARY_STATUS_LABELS[activeTab as LibraryStatus]}»
            ничего нет.
          </p>
        </div>
      )}

      {/* Сетка */}
      {entries.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {entries.map((entry) => (
            <div key={entry.id} className="relative">
              <AnimeCard anime={entry.anime} />
              <div className="absolute top-2 left-2 z-10 px-2 py-1 rounded-lg bg-black/70 backdrop-blur-md border border-white/10 text-xs font-medium text-white">
                {LIBRARY_STATUS_LABELS[entry.status]}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}