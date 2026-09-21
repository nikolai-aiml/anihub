import { useState } from "react";
import { Link } from "react-router-dom";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { reviewsApi } from "../api/reviews";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../contexts/ToastContext";
import {
  ThumbsUpIcon,
  EditIcon,
  TrashIcon,
  StarIcon,
} from "./icons";
import type { Review } from "../types";

interface ReviewCardProps {
  review: Review;
  onEdit?: (review: Review) => void;
}

export function ReviewCard({ review, onEdit }: ReviewCardProps) {
  const { user } = useAuth();
  const { showToast } = useToast();
  const queryClient = useQueryClient();
  const [confirmDelete, setConfirmDelete] = useState(false);

  // ============ ЛАЙК ============
  const likeMutation = useMutation({
    mutationFn: () =>
      review.is_liked
        ? reviewsApi.unlike(review.id)
        : reviewsApi.like(review.id),
    onSuccess: (data) => {
      // Оптимистичное обновление всех списков отзывов
      queryClient.setQueriesData<Review[]>(
        { queryKey: ["reviews", review.anime_id] },
        (old = []) =>
          old.map((r) =>
            r.id === review.id
              ? { ...r, is_liked: data.is_liked, likes_count: data.likes_count }
              : r
          )
      );
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  // ============ УДАЛЕНИЕ ============
  const deleteMutation = useMutation({
    mutationFn: () => reviewsApi.remove(review.id),
    onSuccess: () => {
      queryClient.setQueriesData<Review[]>(
        { queryKey: ["reviews", review.anime_id] },
        (old = []) => old.filter((r) => r.id !== review.id)
      );
      showToast("Отзыв удалён", "success");
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  const handleLike = () => {
    if (!user) {
      showToast("Войдите, чтобы лайкать отзывы", "info");
      return;
    }
    likeMutation.mutate();
  };

  const date = new Date(review.created_at).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  const isEdited = review.updated_at !== review.created_at;

  return (
    <div className="glass rounded-2xl p-5 border border-white/5">
      {/* Заголовок: автор + дата */}
      <div className="flex items-start gap-3 mb-4">
        <Link
          to={`/profile`}
          className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center font-bold text-white flex-shrink-0"
        >
          {review.user.avatar_url ? (
            <img
              src={review.user.avatar_url}
              alt={review.user.username}
              className="w-full h-full rounded-full object-cover"
            />
          ) : (
            review.user.username[0].toUpperCase()
          )}
        </Link>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <Link
              to={`/profile`}
              className="font-medium text-white hover:text-primary transition-colors"
            >
              {review.user.username}
            </Link>
            {review.rating !== null && (
              <span className="flex items-center gap-1 text-xs px-2 py-0.5 rounded-full bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 font-bold">
                <StarIcon className="w-3 h-3" filled />
                {review.rating}
              </span>
            )}
          </div>
          <div className="text-xs text-muted">
            {date}
            {isEdited && <span className="ml-2 italic">(изменён)</span>}
          </div>
        </div>

        {/* Кнопки автора */}
        {review.is_own && (
          <div className="flex items-center gap-1">
            {onEdit && (
              <button
                onClick={() => onEdit(review)}
                className="p-2 rounded-lg text-muted hover:text-primary hover:bg-primary/10 transition-colors"
                title="Редактировать"
              >
                <EditIcon className="w-4 h-4" />
              </button>
            )}
            <button
              onClick={() => setConfirmDelete(true)}
              className="p-2 rounded-lg text-muted hover:text-red-400 hover:bg-red-500/10 transition-colors"
              title="Удалить"
            >
              <TrashIcon className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>

      {/* Текст отзыва */}
      <p className="text-gray-300 leading-relaxed whitespace-pre-wrap">
        {review.text}
      </p>

      {/* Подтверждение удаления */}
      {confirmDelete && (
        <div className="mt-4 p-3 rounded-xl bg-red-500/10 border border-red-500/30 flex items-center justify-between gap-3">
          <span className="text-sm text-red-400">Удалить отзыв?</span>
          <div className="flex gap-2">
            <button
              onClick={() => setConfirmDelete(false)}
              className="px-3 py-1 text-xs rounded-lg text-muted hover:text-white"
            >
              Отмена
            </button>
            <button
              onClick={() => {
                deleteMutation.mutate();
                setConfirmDelete(false);
              }}
              disabled={deleteMutation.isPending}
              className="px-3 py-1 text-xs rounded-lg bg-red-500/20 border border-red-500/50 text-red-400 hover:bg-red-500/30"
            >
              Удалить
            </button>
          </div>
        </div>
      )}

      {/* Лайк */}
      <div className="flex items-center gap-2 mt-4 pt-4 border-t border-white/5">
        <button
          onClick={handleLike}
          disabled={likeMutation.isPending || review.is_own}
          className={`
            inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm
            transition-all duration-200
            ${
              review.is_own
                ? "text-muted cursor-not-allowed opacity-50"
                : review.is_liked
                ? "text-primary bg-primary/10 border border-primary/30"
                : "text-muted hover:text-primary hover:bg-primary/10 border border-transparent"
            }
          `}
          title={review.is_own ? "Нельзя лайкать свой отзыв" : ""}
        >
          <ThumbsUpIcon className="w-4 h-4" filled={review.is_liked} />
          <span>{review.likes_count}</span>
        </button>
      </div>
    </div>
  );
}