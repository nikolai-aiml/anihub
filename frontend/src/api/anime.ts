import { apiClient } from "./client";
import type { AnimeDetail, PaginatedAnime } from "../types";

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
};