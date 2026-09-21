import { apiClient } from "./client";
import type { LibraryEntry, LibraryStats, LibraryStatus } from "../types";

export const libraryApi = {
  async list(status?: LibraryStatus): Promise<LibraryEntry[]> {
    const params = status ? { status } : {};
    const response = await apiClient.get<LibraryEntry[]>("/users/me/library", {
      params,
    });
    return response.data;
  },

  async stats(): Promise<LibraryStats> {
    const response = await apiClient.get<LibraryStats>(
      "/users/me/library/stats"
    );
    return response.data;
  },

  async add(animeId: number, status: LibraryStatus): Promise<LibraryEntry> {
    const response = await apiClient.post<LibraryEntry>(
      `/users/me/library/${animeId}`,
      { status }
    );
    return response.data;
  },

  async updateStatus(
    animeId: number,
    status: LibraryStatus
  ): Promise<LibraryEntry> {
    const response = await apiClient.patch<LibraryEntry>(
      `/users/me/library/${animeId}`,
      { status }
    );
    return response.data;
  },

  async remove(animeId: number): Promise<void> {
    await apiClient.delete(`/users/me/library/${animeId}`);
  },
};