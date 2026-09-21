import { apiClient } from "./client";
import type { Rating, RatingSummary } from "../types";

export const ratingsApi = {
  async summary(animeId: number): Promise<RatingSummary> {
    const response = await apiClient.get<RatingSummary>(
      `/anime/${animeId}/rating`
    );
    return response.data;
  },

  async rate(animeId: number, value: number): Promise<Rating> {
    const response = await apiClient.post<Rating>(
      `/anime/${animeId}/rating`,
      { value }
    );
    return response.data;
  },

  async remove(animeId: number): Promise<void> {
    await apiClient.delete(`/anime/${animeId}/rating`);
  },
};