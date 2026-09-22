import { apiClient } from "./client";
import type { UserDashboard } from "../types";

export const dashboardApi = {
  async get(): Promise<UserDashboard> {
    const response = await apiClient.get<UserDashboard>("/users/me/dashboard");
    return response.data;
  },
};