import { apiClient } from "./client";
import type { AdminAnime, AdminStats, AdminUser } from "../types";

export const adminApi = {
  async stats(): Promise<AdminStats> {
    const response = await apiClient.get<AdminStats>("/admin/stats");
    return response.data;
  },

  async listUsers(): Promise<AdminUser[]> {
    const response = await apiClient.get<AdminUser[]>("/admin/users");
    return response.data;
  },

  async toggleUserActive(userId: number): Promise<AdminUser> {
    const response = await apiClient.patch<AdminUser>(
      `/admin/users/${userId}/toggle-active`
    );
    return response.data;
  },

  async deleteUser(userId: number): Promise<void> {
    await apiClient.delete(`/admin/users/${userId}`);
  },

  async listAnime(): Promise<AdminAnime[]> {
    const response = await apiClient.get<AdminAnime[]>("/admin/anime");
    return response.data;
  },

  async deleteAnime(animeId: number): Promise<void> {
    await apiClient.delete(`/admin/anime/${animeId}`);
  },
};