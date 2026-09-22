import { apiClient } from "./client";
import type { Notification, UnreadCount } from "../types";

export const notificationsApi = {
  async list(): Promise<Notification[]> {
    const response = await apiClient.get<Notification[]>(
      "/users/me/notifications"
    );
    return response.data;
  },

  async unreadCount(): Promise<UnreadCount> {
    const response = await apiClient.get<UnreadCount>(
      "/users/me/notifications/unread-count"
    );
    return response.data;
  },

  async markRead(id: number): Promise<void> {
    await apiClient.patch(`/users/me/notifications/${id}/read`);
  },

  async markAllRead(): Promise<void> {
    await apiClient.patch("/users/me/notifications/read-all");
  },
};