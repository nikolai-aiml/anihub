import { apiClient } from "./client";
import type { UserAchievement } from "../types";

export const achievementsApi = {
  async list(): Promise<UserAchievement[]> {
    const response = await apiClient.get<UserAchievement[]>(
      "/users/me/achievements"
    );
    return response.data;
  },

  async check(): Promise<string[]> {
    const response = await apiClient.post<string[]>(
      "/users/me/achievements/check"
    );
    return response.data;
  },
};