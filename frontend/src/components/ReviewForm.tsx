import { useState, type FormEvent } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { reviewsApi } from "../api/reviews";
import { useToast } from "../contexts/ToastContext";
import { StarRating } from "./StarRating";
import type { Review } from "../types";

interface ReviewFormProps {
  animeId: number;
  editingReview?: Review | null;
  onCancelEdit?: () => void;
}

export function ReviewForm({
  animeId,
  editingReview = null,
  onCancelEdit,
}: ReviewFormProps) {
  const { showToast } = useToast();
  const queryClient = useQueryClient();

  const [text, setText] = useState(editingReview?.text ?? "");
  const [rating, setRating] = useState<number | null>(
    editingReview?.rating ?? null
  );

  const isEditing = !!editingReview;

  const createMutation = useMutation({
    mutationFn: () => reviewsApi.create(animeId, { text, rating }),
    onSuccess: (newReview) => {
      queryClient.setQueriesData<Review[]>(
        { queryKey: ["reviews", animeId] },
        (old = []) => [newReview, ...old]
      );
      queryClient.invalidateQueries({ queryKey: ["reviews", animeId] });
      showToast("Отзыв опубликован", "success");
      setText("");
      setRating(null);
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  const updateMutation = useMutation({
    mutationFn: () =>
      reviewsApi.update(editingReview!.id, { text, rating }),
    onSuccess: (updated) => {
      queryClient.setQueriesData<Review[]>(
        { queryKey: ["reviews", animeId] },
        (old = []) =>
          old.map((r) => (r.id === updated.id ? updated : r))
      );
      showToast("Отзыв обновлён", "success");
      onCancelEdit?.();
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (text.trim().length < 10) {
      showToast("Отзыв должен быть минимум 10 символов", "error");
      return;
    }
    if (isEditing) {
      updateMutation.mutate();
    } else {
      createMutation.mutate();
    }
  };

  const isPending = createMutation.isPending || updateMutation.isPending;

  return (
    <form
      onSubmit={handleSubmit}
      className="glass rounded-2xl p-5 border border-white/5"
    >
      <h3 className="text-lg font-bold font-display mb-4">
        {isEditing ? "Редактировать отзыв" : "Оставить отзыв"}
      </h3>

      {/* Оценка */}
      <div className="mb-4">
        <label className="block text-sm text-gray-300 mb-2">
          Оценка (опционально)
        </label>
        <StarRating
          value={rating}
          onChange={setRating}
          size="md"
        />
      </div>

      {/* Текст */}
      <div className="mb-4">
        <label className="block text-sm text-gray-300 mb-2">
          Отзыв
        </label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Поделитесь впечатлениями об аниме..."
          rows={5}
          maxLength={2000}
          className="input resize-none"
          disabled={isPending}
        />
        <div className="text-xs text-muted mt-1 text-right">
          {text.length} / 2000
        </div>
      </div>

      {/* Кнопки */}
      <div className="flex gap-3">
        <button
          type="submit"
          disabled={isPending || text.trim().length < 10}
          className="btn-primary flex-1"
        >
          {isPending
            ? "Сохранение..."
            : isEditing
            ? "Сохранить"
            : "Опубликовать"}
        </button>

        {isEditing && onCancelEdit && (
          <button
            type="button"
            onClick={onCancelEdit}
            className="btn-ghost"
            disabled={isPending}
          >
            Отмена
          </button>
        )}
      </div>
    </form>
  );
}