import { apiClient } from "./client";
import type {
  LoginCredentials,
  RegisterData,
  TokenResponse,
  User,
} from "../types";

export const authApi = {
  async register(data: RegisterData): Promise<User> {
    const response = await apiClient.post<User>("/auth/register", data);
    return response.data;
    
  },
  async changePassword(data: {
    old_password: string;
    new_password: string;
    new_password_confirm: string;
  }): Promise<void> {
    await apiClient.post("/users/me/change-password", data);
  },
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const params = new URLSearchParams();
    params.append("username", credentials.username);
    params.append("password", credentials.password);

    const response = await apiClient.post<TokenResponse>("/auth/login", params, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return response.data;
  },

  async getMe(): Promise<User> {
    const response = await apiClient.get<User>("/users/me");
    return response.data;
  },

  async updateMe(data: Partial<User>): Promise<User> {
    const response = await apiClient.patch<User>("/users/me", data);
    return response.data;
  },
};