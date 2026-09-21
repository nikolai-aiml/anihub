import { apiClient } from "./client";
import type {
  Review,
  ReviewCreate,
  ReviewLikeStatus,
} from "../types";

export const reviewsApi = {
  async list(
    animeId: number,
    sort: "new" | "popular" = "new"
  ): Promise<Review[]> {
    const response = await apiClient.get<Review[]>(
      `/anime/${animeId}/reviews`,
      { params: { sort } }
    );
    return response.data;
  },

  async create(animeId: number, data: ReviewCreate): Promise<Review> {
    const response = await apiClient.post<Review>(
      `/anime/${animeId}/reviews`,
      data
    );
    return response.data;
  },

  async update(
    reviewId: number,
    data: Partial<ReviewCreate>
  ): Promise<Review> {
    const response = await apiClient.patch<Review>(
      `/reviews/${reviewId}`,
      data
    );
    return response.data;
  },

  async remove(reviewId: number): Promise<void> {
    await apiClient.delete(`/reviews/${reviewId}`);
  },

  async like(reviewId: number): Promise<ReviewLikeStatus> {
    const response = await apiClient.post<ReviewLikeStatus>(
      `/reviews/${reviewId}/like`
    );
    return response.data;
  },

  async unlike(reviewId: number): Promise<ReviewLikeStatus> {
    const response = await apiClient.delete<ReviewLikeStatus>(
      `/reviews/${reviewId}/like`
    );
    return response.data;
  },
};