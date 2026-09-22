import { useState, useRef, useEffect } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { libraryApi } from "../api/library";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../contexts/ToastContext";
import {
  LIBRARY_STATUS_LABELS,
  type LibraryEntry,
  type LibraryStatus,
} from "../types";
import { BookIcon, CloseIcon } from "./icons";

interface LibraryButtonProps {
  animeId: number;
}

const ALL_STATUSES: LibraryStatus[] = [
  "watching",
  "planned",
  "completed",
  "on_hold",
  "dropped",
];

export function LibraryButton({ animeId }: LibraryButtonProps) {
  const { user } = useAuth();
  const { showToast } = useToast();
  const queryClient = useQueryClient();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Получаем библиотеку — находим запись для этого аниме
  const { data: library = [] } = useQuery<LibraryEntry[]>({
    queryKey: ["library", "all"],
    queryFn: () => libraryApi.list(),
    enabled: !!user,
  });

  const currentEntry = library.find((e) => e.anime_id === animeId);
  const currentStatus = currentEntry?.status;

  // Закрытие dropdown при клике вне
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node)
      ) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Добавить
    const addMutation = useMutation({
    mutationFn: (status: LibraryStatus) => libraryApi.add(animeId, status),
    onSuccess: (entry) => {
      queryClient.setQueryData<LibraryEntry[]>(["library", "all"], (old = []) => [
        ...old,
        entry,
      ]);
      queryClient.invalidateQueries({ queryKey: ["library", "stats"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });   // ← ДОБАВЬ
      showToast(`Добавлено: ${LIBRARY_STATUS_LABELS[entry.status]}`, "success");
      setIsOpen(false);
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  const updateMutation = useMutation({
    mutationFn: (status: LibraryStatus) =>
      libraryApi.updateStatus(animeId, status),
    onSuccess: (entry) => {
      queryClient.setQueryData<LibraryEntry[]>(["library", "all"], (old = []) =>
        old.map((e) => (e.anime_id === animeId ? entry : e))
      );
      queryClient.invalidateQueries({ queryKey: ["library", "stats"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });   // ← ДОБАВЬ
      showToast(`Статус: ${LIBRARY_STATUS_LABELS[entry.status]}`, "success");
      setIsOpen(false);
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  const removeMutation = useMutation({
    mutationFn: () => libraryApi.remove(animeId),
    onSuccess: () => {
      queryClient.setQueryData<LibraryEntry[]>(["library", "all"], (old = []) =>
        old.filter((e) => e.anime_id !== animeId)
      );
      queryClient.invalidateQueries({ queryKey: ["library", "stats"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });   // ← ДОБАВЬ
      showToast("Удалено из библиотеки", "success");
      setIsOpen(false);
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  const handleSelect = (status: LibraryStatus) => {
    if (!user) {
      showToast("Войдите, чтобы добавить в библиотеку", "info");
      return;
    }
    if (currentStatus === status) {
      setIsOpen(false);
      return;
    }
    if (currentEntry) {
      updateMutation.mutate(status);
    } else {
      addMutation.mutate(status);
    }
  };

  const handleRemove = () => {
    if (!user) return;
    removeMutation.mutate();
  };

  const isPending =
    addMutation.isPending ||
    updateMutation.isPending ||
    removeMutation.isPending;

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Основная кнопка */}
      <button
        onClick={() => {
          if (!user) {
            showToast("Войдите, чтобы добавить в библиотеку", "info");
            return;
          }
          setIsOpen(!isOpen);
        }}
        disabled={isPending}
        className={`
          inline-flex items-center gap-2 px-5 py-3 rounded-xl font-medium
          transition-all duration-300
          ${
            currentStatus
              ? "bg-primary/20 border border-primary/50 text-primary hover:bg-primary/30"
              : "glass-button hover:bg-primary/25 hover:border-primary/50"
          }
        `}
      >
        <BookIcon className="w-5 h-5" />
        {currentStatus ? LIBRARY_STATUS_LABELS[currentStatus] : "В библиотеку"}
      </button>

      {/* Dropdown */}
      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-56 z-50 glass-strong rounded-xl border border-white/10 shadow-2xl overflow-hidden animate-fade-in">
          {ALL_STATUSES.map((status) => (
            <button
              key={status}
              onClick={() => handleSelect(status)}
              className={`
                w-full text-left px-4 py-2.5 text-sm transition-colors
                ${
                  currentStatus === status
                    ? "bg-primary/20 text-primary"
                    : "text-gray-300 hover:bg-white/5 hover:text-white"
                }
              `}
            >
              {LIBRARY_STATUS_LABELS[status]}
            </button>
          ))}

          {currentEntry && (
            <>
              <div className="border-t border-white/10" />
              <button
                onClick={handleRemove}
                className="w-full text-left px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/10 transition-colors flex items-center gap-2"
              >
                <CloseIcon className="w-4 h-4" />
                Удалить из библиотеки
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}