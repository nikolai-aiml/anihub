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
// Library
export type LibraryStatus =
  | "planned"
  | "watching"
  | "completed"
  | "on_hold"
  | "dropped";

export interface LibraryEntry {
  id: number;
  anime_id: number;
  status: LibraryStatus;
  created_at: string;
  updated_at: string;
  anime: AnimeListItem;
}

export interface LibraryStats {
  planned: number;
  watching: number;
  completed: number;
  on_hold: number;
  dropped: number;
}

export const LIBRARY_STATUS_LABELS: Record<LibraryStatus, string> = {
  planned: "Буду смотреть",
  watching: "Смотрю",
  completed: "Завершено",
  on_hold: "Отложено",
  dropped: "Брошено",
};

export const LIBRARY_STATUS_COLORS: Record<LibraryStatus, string> = {
  planned: "text-blue-400 bg-blue-500/10 border-blue-500/30",
  watching: "text-purple-400 bg-purple-500/10 border-purple-500/30",
  completed: "text-green-400 bg-green-500/10 border-green-500/30",
  on_hold: "text-yellow-400 bg-yellow-500/10 border-yellow-500/30",
  dropped: "text-red-400 bg-red-500/10 border-red-500/30",
};
// Ratings
export interface Rating {
  id: number;
  anime_id: number;
  value: number;
  created_at: string;
  updated_at: string;
}

export interface RatingSummary {
  average: number;
  count: number;
  user_rating: number | null;
}
// Reviews
export interface ReviewAuthor {
  id: number;
  username: string;
  avatar_url: string | null;
}

export interface Review {
  id: number;
  anime_id: number;
  rating: number | null;
  text: string;
  likes_count: number;
  created_at: string;
  updated_at: string;
  user: ReviewAuthor;
  is_liked: boolean;
  is_own: boolean;
}

export interface ReviewCreate {
  text: string;
  rating?: number | null;
}

export interface ReviewLikeStatus {
  is_liked: boolean;
  likes_count: number;
}
// Profile
export interface ProfileStats {
  library_total: number;
  ratings_total: number;
  reviews_total: number;
  favorites_total: number;
}

export interface Profile {
  id: number;
  username: string;
  email: string;
  avatar_url: string | null;
  bio: string | null;
  created_at: string;
  stats: ProfileStats;
}
// Achievements
export type AchievementRarity = "common" | "rare" | "epic" | "legendary";
export type AchievementCategory =
  | "library"
  | "ratings"
  | "reviews"
  | "favorites"
  | "special";

export interface UserAchievement {
  id: number;
  code: string;
  title: string;
  description: string;
  icon: string;
  rarity: AchievementRarity;
  category: AchievementCategory;
  target: number;
  progress: number;
  is_unlocked: boolean;
  unlocked_at: string | null;
}

export const RARITY_LABELS: Record<AchievementRarity, string> = {
  common: "Обычное",
  rare: "Редкое",
  epic: "Эпическое",
  legendary: "Легендарное",
};

export const RARITY_COLORS: Record<AchievementRarity, string> = {
  common: "text-gray-300 border-gray-500/30 bg-gray-500/10",
  rare: "text-blue-400 border-blue-500/30 bg-blue-500/10",
  epic: "text-purple-400 border-purple-500/30 bg-purple-500/10",
  legendary: "text-yellow-400 border-yellow-500/30 bg-yellow-500/10",
};
// Notifications
export type NotificationType =
  | "achievement"
  | "review_like"
  | "library_add"
  | "favorite_add"
  | "system";

export interface Notification {
  id: number;
  type: NotificationType;
  title: string;
  message: string;
  link: string | null;
  is_read: boolean;
  created_at: string;
}

export interface UnreadCount {
  count: number;
}