import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { notificationsApi } from "../api/notifications";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../contexts/ToastContext";
import type { Notification, UnreadCount } from "../types";

export function useNotifications() {
  const { user } = useAuth();

  return useQuery<Notification[]>({
    queryKey: ["notifications", user?.id ?? "me"],
    queryFn: () => notificationsApi.list(),
    enabled: !!user,
    refetchInterval: 30_000,   // обновление каждые 30 сек
  });
}

export function useUnreadCount() {
  const { user } = useAuth();

  return useQuery<UnreadCount>({
    queryKey: ["notifications", "unread", user?.id ?? "me"],
    queryFn: () => notificationsApi.unreadCount(),
    enabled: !!user,
    refetchInterval: 30_000,
  });
}

export function useNotificationActions() {
  const queryClient = useQueryClient();
  const { showToast } = useToast();

  const markRead = useMutation({
    mutationFn: (id: number) => notificationsApi.markRead(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] });
    },
  });

  const markAllRead = useMutation({
    mutationFn: () => notificationsApi.markAllRead(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] });
      showToast("Все уведомления прочитаны", "success");
    },
  });

  return { markRead, markAllRead };
}