import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Navigate } from "react-router-dom";
import { adminApi } from "../api/admin";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../contexts/ToastContext";
import { Loader } from "../components/Loader";
import { TrashIcon } from "../components/icons";
import type { AdminAnime, AdminUser } from "../types";

type Tab = "stats" | "users" | "anime";

export function Admin() {
  const { user } = useAuth();
  const { showToast } = useToast();
  const queryClient = useQueryClient();
  const [tab, setTab] = useState<Tab>("stats");

  // Редирект, если не админ
  if (!user?.is_superuser) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="container mx-auto px-6 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-display">Админ-панель</h1>
        <p className="text-muted text-sm mt-1">
          Управление пользователями и контентом
        </p>
      </div>

      <div className="flex flex-wrap gap-2 mb-8">
        {[
          { value: "stats", label: "Статистика" },
          { value: "users", label: "Пользователи" },
          { value: "anime", label: "Аниме" },
        ].map((t) => (
          <button
            key={t.value}
            onClick={() => setTab(t.value as Tab)}
            className={`
              px-5 py-2.5 rounded-xl text-sm font-medium transition-all
              ${
                tab === t.value
                  ? "bg-primary/20 text-primary border border-primary/40"
                  : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
              }
            `}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === "stats" && <StatsTab />}
      {tab === "users" && <UsersTab />}
      {tab === "anime" && <AnimeTab />}
    </div>
  );
}

// ============ STATS ============
function StatsTab() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ["admin-stats"],
    queryFn: () => adminApi.stats(),
  });

  if (isLoading) return <Loader />;
  if (!stats) return null;

  const cards = [
    { label: "Пользователи", value: stats.users_total, icon: "👥" },
    { label: "Активные", value: stats.users_active, icon: "✅" },
    { label: "Аниме", value: stats.anime_total, icon: "🎬" },
    { label: "Отзывы", value: stats.reviews_total, icon: "💬" },
    { label: "Оценки", value: stats.ratings_total, icon: "⭐" },
    { label: "Избранное", value: stats.favorites_total, icon: "❤️" },
    { label: "Библиотека", value: stats.library_total, icon: "📚" },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className="glass rounded-2xl p-5 border border-white/5"
        >
          <div className="text-3xl mb-2">{card.icon}</div>
          <div className="text-3xl font-bold font-display tabular-nums">
            {card.value}
          </div>
          <div className="text-xs text-muted mt-1">{card.label}</div>
        </div>
      ))}
    </div>
  );
}

// ============ USERS ============
function UsersTab() {
  const { showToast } = useToast();
  const queryClient = useQueryClient();
  const [confirmDelete, setConfirmDelete] = useState<number | null>(null);

  const { data: users = [], isLoading } = useQuery<AdminUser[]>({
    queryKey: ["admin-users"],
    queryFn: () => adminApi.listUsers(),
  });

  const toggleMutation = useMutation({
    mutationFn: (id: number) => adminApi.toggleUserActive(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin-users"] });
      showToast("Статус обновлён", "success");
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => adminApi.deleteUser(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin-users"] });
      showToast("Пользователь удалён", "success");
      setConfirmDelete(null);
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  if (isLoading) return <Loader />;

  return (
    <div className="space-y-3">
      {users.map((u) => (
        <div
          key={u.id}
          className="glass rounded-xl p-4 border border-white/5 flex items-center justify-between gap-4"
        >
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="font-medium">{u.username}</span>
              {u.is_superuser && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-primary/20 text-primary border border-primary/30">
                  админ
                </span>
              )}
              {!u.is_active && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/30">
                  заблокирован
                </span>
              )}
            </div>
            <p className="text-xs text-muted mt-1">{u.email}</p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => toggleMutation.mutate(u.id)}
              className="px-3 py-1.5 rounded-lg text-xs glass-button hover:bg-primary/25"
            >
              {u.is_active ? "Заблокировать" : "Разблокировать"}
            </button>

            {confirmDelete === u.id ? (
              <>
                <button
                  onClick={() => deleteMutation.mutate(u.id)}
                  className="px-3 py-1.5 rounded-lg text-xs bg-red-500/20 border border-red-500/50 text-red-400"
                >
                  Точно
                </button>
                <button
                  onClick={() => setConfirmDelete(null)}
                  className="px-3 py-1.5 rounded-lg text-xs text-muted"
                >
                  Отмена
                </button>
              </>
            ) : (
              <button
                onClick={() => setConfirmDelete(u.id)}
                className="p-2 rounded-lg text-muted hover:text-red-400 hover:bg-red-500/10"
              >
                <TrashIcon className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

// ============ ANIME ============
function AnimeTab() {
  const { showToast } = useToast();
  const queryClient = useQueryClient();
  const [confirmDelete, setConfirmDelete] = useState<number | null>(null);

  const { data: anime = [], isLoading } = useQuery<AdminAnime[]>({
    queryKey: ["admin-anime"],
    queryFn: () => adminApi.listAnime(),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => adminApi.deleteAnime(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin-anime"] });
      showToast("Аниме удалено", "success");
      setConfirmDelete(null);
    },
  });

  if (isLoading) return <Loader />;

  return (
    <div className="space-y-3">
      {anime.map((a) => (
        <div
          key={a.id}
          className="glass rounded-xl p-4 border border-white/5 flex items-center justify-between gap-4"
        >
          <div className="flex-1 min-w-0">
            <span className="font-medium">{a.title}</span>
            <p className="text-xs text-muted mt-1">
              {a.title_en} · {a.year} · ⭐ {a.rating.toFixed(1)} ({a.rating_count})
            </p>
          </div>

          {confirmDelete === a.id ? (
            <div className="flex items-center gap-2">
              <button
                onClick={() => deleteMutation.mutate(a.id)}
                className="px-3 py-1.5 rounded-lg text-xs bg-red-500/20 border border-red-500/50 text-red-400"
              >
                Точно
              </button>
              <button
                onClick={() => setConfirmDelete(null)}
                className="px-3 py-1.5 rounded-lg text-xs text-muted"
              >
                Отмена
              </button>
            </div>
          ) : (
            <button
              onClick={() => setConfirmDelete(a.id)}
              className="p-2 rounded-lg text-muted hover:text-red-400 hover:bg-red-500/10"
            >
              <TrashIcon className="w-4 h-4" />
            </button>
          )}
        </div>
      ))}
    </div>
  );
}