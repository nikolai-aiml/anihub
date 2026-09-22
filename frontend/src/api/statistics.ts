import { apiClient } from "./client";
import type { UserStatistics } from "../types";

export const statisticsApi = {
  async getMe(): Promise<UserStatistics> {
    const response = await apiClient.get<UserStatistics>(
      "/users/me/statistics"
    );
    return response.data;
  },
};