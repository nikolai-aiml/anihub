import { apiClient } from "./client";
import type { Profile } from "../types";

export const profileApi = {
  async getMe(): Promise<Profile> {
    const response = await apiClient.get<Profile>("/users/me/profile");
    return response.data;
  },
};