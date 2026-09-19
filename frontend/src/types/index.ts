export interface User {
  id: number;
  username: string;
  email: string;
  avatar_url: string | null;
  bio: string | null;
  is_active: boolean;
  created_at: string;
}

export interface Genre {
  id: number;
  name: string;
  slug: string;
}

export type AnimeType = "tv" | "movie" | "ova" | "ona" | "special";
export type AnimeStatus = "ongoing" | "completed" | "upcoming";

export interface AnimeListItem {
  id: number;
  title: string;
  title_en: string | null;
  poster_url: string | null;
  year: number | null;
  type: AnimeType;
  status: AnimeStatus;
  episodes_total: number | null;
  rating: number;
  rating_count: number;
  genres: Genre[];
}

export interface AnimeDetail extends AnimeListItem {
  title_jp: string | null;
  alternative_titles: string | null;
  description: string | null;
  duration_minutes: number | null;
  studio: string | null;
  created_at: string;
  updated_at: string;
}

export interface PaginatedAnime {
  items: AnimeListItem[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
}