import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ratingsApi } from "../api/ratings";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../contexts/ToastContext";
import type { RatingSummary } from "../types";

export function useRating(animeId: number) {
  const { user } = useAuth();
  const { showToast } = useToast();
  const queryClient = useQueryClient();

  const query = useQuery<RatingSummary>({
    queryKey: ["rating", animeId],
    queryFn: () => ratingsApi.summary(animeId),
    enabled: !isNaN(animeId),
  });

  const rateMutation = useMutation({
    mutationFn: (value: number) => ratingsApi.rate(animeId, value),
    onSuccess: async (_, value) => {
      // Перезапрашиваем сводку
      await queryClient.refetchQueries({ queryKey: ["rating", animeId] });
      // Инвалидируем кэш аниме (общий рейтинг изменился)
      queryClient.invalidateQueries({ queryKey: ["anime", animeId] });
      showToast(`Оценка сохранена: ${value}/10`, "success");
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  const removeMutation = useMutation({
    mutationFn: () => ratingsApi.remove(animeId),
    onSuccess: async () => {
      await queryClient.refetchQueries({ queryKey: ["rating", animeId] });
      queryClient.invalidateQueries({ queryKey: ["anime", animeId] });
      showToast("Оценка удалена", "success");
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  const handleRate = (value: number) => {
    if (!user) {
      showToast("Войдите, чтобы поставить оценку", "info");
      return;
    }
    rateMutation.mutate(value);
  };

  const handleRemove = () => {
    if (!user) return;
    removeMutation.mutate();
  };

  return {
    summary: query.data,
    isLoading: query.isLoading,
    isPending: rateMutation.isPending || removeMutation.isPending,
    rate: handleRate,
    remove: handleRemove,
  };
}