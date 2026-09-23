import { apiClient } from "./client";
import type {
  AnimeDetail,
  AnimeListItem,
  Episode,
  PaginatedAnime,
} from "../types";

export interface AnimeListParams {
  page?: number;
  size?: number;
  sort?: string;
  order?: "asc" | "desc";
  search?: string;
  genre?: string;
  year?: number;
  type?: string;
  status?: string;
  studio?: string;
}

export const animeApi = {
  async list(params: AnimeListParams = {}): Promise<PaginatedAnime> {
    const response = await apiClient.get<PaginatedAnime>("/anime", { params });
    return response.data;
  },

  async getById(id: number): Promise<AnimeDetail> {
    const response = await apiClient.get<AnimeDetail>(`/anime/${id}`);
    return response.data;
  },

  async spotlight(): Promise<{
    top_month: AnimeListItem[];
    new_season: AnimeListItem[];
  }> {
    const response = await apiClient.get("/anime/spotlight");
    return response.data;
  },

  async listEpisodes(animeId: number): Promise<Episode[]> {
    const response = await apiClient.get<Episode[]>(
      `/anime/${animeId}/episodes`
    );
    return response.data;
  },

  async getEpisode(animeId: number, number: number): Promise<Episode> {
    const response = await apiClient.get<Episode>(
      `/anime/${animeId}/episodes/${number}`
    );
    return response.data;
  },
};