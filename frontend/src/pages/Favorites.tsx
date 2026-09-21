import { Link } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { favoritesApi } from "../api/favorites";
import { AnimeCard } from "../components/AnimeCard";
import { Loader } from "../components/Loader";
import { HeartIcon, ArrowRightIcon } from "../components/icons";
import { useToast } from "../contexts/ToastContext";

export function Favorites() {
  const { showToast } = useToast();
  const queryClient = useQueryClient();

  const { data: favorites = [], isLoading } = useQuery({
    queryKey: ["favorites"],
    queryFn: () => favoritesApi.list(),
  });

    const removeMutation = useMutation({
    mutationFn: (animeId: number) => favoritesApi.remove(animeId),
    onSuccess: async () => {
        await queryClient.refetchQueries({ queryKey: ["favorites"] });
        showToast("Удалено из избранного", "success");
    },
    onError: (err: any) => {
        showToast(err.response?.data?.detail || "Ошибка", "error");
    },
    });

  if (isLoading) return <Loader />;

  // Пустое состояние
  if (favorites.length === 0) {
    return (
      <div className="container mx-auto px-6 py-20 text-center">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-primary/10 border border-primary/20 mb-6">
          <HeartIcon className="w-10 h-10 text-primary" />
        </div>
        <h1 className="text-3xl font-bold font-display mb-3">
          Здесь пока ничего нет
        </h1>
        <p className="text-muted max-w-md mx-auto mb-8">
          Добавь аниме, чтобы собрать свою коллекцию.
        </p>
        <Link to="/catalog" className="btn-primary inline-flex items-center gap-2">
          Открыть каталог
          <ArrowRightIcon className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold font-display">Избранное</h1>
          <p className="text-muted text-sm mt-1">
            {favorites.length} {favorites.length === 1 ? "аниме" : "аниме"}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {favorites.map((fav) => (
          <div key={fav.id} className="group relative">
            <AnimeCard anime={fav.anime} />

            {/* Кнопка удаления поверх карточки */}
            <button
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                removeMutation.mutate(fav.anime_id);
              }}
              className="
                absolute top-2 left-2 z-10
                w-9 h-9 rounded-full
                bg-black/70 backdrop-blur-md
                border border-white/20
                flex items-center justify-center
                text-accent
                opacity-0 group-hover:opacity-100
                hover:bg-accent hover:text-white
                transition-all duration-300
              "
              aria-label="Удалить из избранного"
            >
              <HeartIcon className="w-4 h-4" filled />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}