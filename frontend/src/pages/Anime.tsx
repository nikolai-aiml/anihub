import { useParams, Link } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { animeApi } from "../api/anime";
import { favoritesApi } from "../api/favorites";
import { Loader } from "../components/Loader";
import { HeartIcon } from "../components/icons";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../contexts/ToastContext";
import { LibraryButton } from "../components/LibraryButton";
import { useRating } from "../hooks/useRating";
import { StarRating } from "../components/StarRating";
import { useState } from "react";
import { reviewsApi } from "../api/reviews";
import { ReviewCard } from "../components/ReviewCard";
import { ReviewForm } from "../components/ReviewForm";
import type { Review } from "../types";
import { translateGenre } from "../types";
import { useQuery } from "@tanstack/react-query";

export function Anime() {
  const { id } = useParams<{ id: string }>();
  const animeId = Number(id);
  const { user } = useAuth();
  const { showToast } = useToast();
  const queryClient = useQueryClient();
  

  const {
    summary: rating,
    isPending: ratingPending,
    rate: handleRate,
    remove: handleRemoveRating,
} = useRating(animeId);
// Проверяем наличие эпизодов
const { data: episodes = [] } = useQuery({
  queryKey: ["episodes", animeId],
  queryFn: () => animeApi.listEpisodes(animeId),
  enabled: !isNaN(animeId),
});

  // Отзывы
  const [reviewSort, setReviewSort] = useState<"new" | "popular">("new");
  const [editingReview, setEditingReview] = useState<Review | null>(null);

  const { data: reviews = [] } = useQuery({
    queryKey: ["reviews", animeId, reviewSort],
    queryFn: () => reviewsApi.list(animeId, reviewSort),
    enabled: !isNaN(animeId),
  });

  const myReview = reviews.find((r) => r.is_own);
  const otherReviews = reviews.filter((r) => !r.is_own);

  // Аниме
  const { data: anime, isLoading, error } = useQuery({
    queryKey: ["anime", animeId],
    queryFn: () => animeApi.getById(animeId),
    enabled: !isNaN(animeId),
  });

  // Избранное
  const { data: favorites = [] } = useQuery({
    queryKey: ["favorites"],
    queryFn: () => favoritesApi.list(),
    enabled: !!user,
  });

  const isFavorite = favorites.some((f) => f.anime_id === animeId);

  // Добавить
  const addMutation = useMutation({
    mutationFn: () => favoritesApi.add(animeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["favorites"] });
      showToast("Добавлено в избранное", "success");
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  // Удалить
  const removeMutation = useMutation({
    mutationFn: () => favoritesApi.remove(animeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["favorites"] });
      showToast("Удалено из избранного", "success");
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  const handleFavoriteToggle = () => {
    if (!user) {
      showToast("Войдите, чтобы добавить в избранное", "info");
      return;
    }
    if (isFavorite) {
      removeMutation.mutate();
    } else {
      addMutation.mutate();
    }
  };

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
              ⭐ {rating ? rating.average.toFixed(1) : anime.rating.toFixed(1)}
            </span>
            <span className="text-muted">
              {rating ? rating.count : anime.rating_count} оценок
            </span>
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
                {translateGenre(g.slug)}
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
            {/* Оценка */}
            <div className="mt-6 p-4 rounded-xl bg-surface/50 border border-white/5">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-medium text-gray-300">
                  Ваша оценка
                </span>
                {rating?.user_rating && (
                  <span className="text-xs text-muted">
                    Оценено
                  </span>
                )}
              </div>
              <StarRating
                value={rating?.user_rating ?? null}
                onChange={handleRate}
                onRemove={handleRemoveRating}
                disabled={ratingPending}
                size="lg"
              />
              </div>
                    {/* ============ ОТЗЫВЫ ============ */}
        <div className="mt-12 pt-8 border-t border-white/10">
          <h2 className="text-2xl font-bold font-display mb-6">
            Отзывы
            {reviews.length > 0 && (
              <span className="text-muted text-base font-normal ml-2">
                ({reviews.length})
              </span>
            )}
          </h2>

          {/* Форма — только для авторизованных */}
          {user && !myReview && !editingReview && (
            <div className="mb-6">
              <ReviewForm animeId={animeId} />
            </div>
          )}

          {/* Редактирование своего отзыва */}
          {user && editingReview && (
            <div className="mb-6">
              <ReviewForm
                animeId={animeId}
                editingReview={editingReview}
                onCancelEdit={() => setEditingReview(null)}
              />
            </div>
          )}

          {/* Сортировка */}
          {reviews.length > 1 && (
            <div className="flex gap-2 mb-4">
              {(["new", "popular"] as const).map((s) => (
                <button
                  key={s}
                  onClick={() => setReviewSort(s)}
                  className={`
                    px-4 py-2 rounded-xl text-sm font-medium transition-all
                    ${
                      reviewSort === s
                        ? "bg-primary/20 text-primary border border-primary/40"
                        : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
                    }
                  `}
                >
                  {s === "new" ? "Новые" : "Популярные"}
                </button>
              ))}
            </div>
          )}

          {/* Список отзывов */}
          {reviews.length === 0 && (
            <div className="text-center py-12 text-muted">
              Пока нет отзывов. Будь первым!
            </div>
          )}

          <div className="space-y-4">
            {myReview && (
              <ReviewCard
                review={myReview}
                onEdit={(r) => setEditingReview(r)}
              />
            )}
            {otherReviews.map((review) => (
              <ReviewCard key={review.id} review={review} />
            ))}
          </div>
        </div>
          {/* Кнопки */}
          <div className="flex flex-wrap gap-3 mt-8">
            {/* Кнопка "Смотреть" — только если есть эпизоды */}
            {episodes.length > 0 && (
              <Link
                to={`/watch/${anime.id}/1`}
                className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-primary to-accent hover:from-primary-hover hover:to-pink-600 text-white font-semibold transition-all duration-300 hover:scale-105 active:scale-95 shadow-lg shadow-primary/30"
              >
                ▶ Смотреть
              </Link>
            )}

            {/* В избранное */}
            <button
              onClick={handleFavoriteToggle}
              disabled={addMutation.isPending || removeMutation.isPending}
              className={`
                inline-flex items-center gap-2 px-5 py-3 rounded-xl font-medium
                transition-all duration-300
                ${
                  isFavorite
                    ? "bg-accent/20 border border-accent/50 text-accent hover:bg-accent/30"
                    : "glass-button hover:bg-primary/25 hover:border-primary/50"
                }
              `}
            >
              <HeartIcon className="w-5 h-5" filled={isFavorite} />
              {isFavorite ? "В избранном" : "В избранное"}
            </button>

            {/* В библиотеку */}
            <LibraryButton animeId={animeId} />
          </div>
        </div>
      </div>
    </div>
  );
}