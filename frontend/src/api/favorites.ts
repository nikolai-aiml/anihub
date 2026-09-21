import { apiClient } from "./client";
import type { AnimeListItem } from "../types";

export interface Favorite {
  id: number;
  anime_id: number;
  created_at: string;
  anime: AnimeListItem;
}

export const favoritesApi = {
  async list(): Promise<Favorite[]> {
    const response = await apiClient.get<Favorite[]>("/users/me/favorites");
    return response.data;
  },

  async add(animeId: number): Promise<Favorite> {
    const response = await apiClient.post<Favorite>(
      `/users/me/favorites/${animeId}`
    );
    return response.data;
  },

  async remove(animeId: number): Promise<void> {
    await apiClient.delete(`/users/me/favorites/${animeId}`);
  },
};