import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { animeApi } from "../api/anime";
import { Loader } from "../components/Loader";
import { ArrowRightIcon } from "../components/icons";

export function Watch() {
  const { animeId, episodeNumber } = useParams<{
    animeId: string;
    episodeNumber: string;
  }>();

  const id = Number(animeId);
  const num = Number(episodeNumber);

  const { data: anime } = useQuery({
    queryKey: ["anime", id],
    queryFn: () => animeApi.getById(id),
    enabled: !isNaN(id),
  });

  const {
    data: episode,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["episode", id, num],
    queryFn: () => animeApi.getEpisode(id, num),
    enabled: !isNaN(id) && !isNaN(num),
  });

  const { data: episodes = [] } = useQuery({
    queryKey: ["episodes", id],
    queryFn: () => animeApi.listEpisodes(id),
    enabled: !isNaN(id),
  });

  if (isLoading) return <Loader />;

  if (error || !episode || !anime) {
    return (
      <div className="container mx-auto px-6 py-20 text-center">
        <p className="text-muted mb-4">Эпизод не найден</p>
        <Link to={`/anime/${id}`} className="btn-primary inline-block">
          Вернуться к аниме
        </Link>
      </div>
    );
  }

  const videoSrc = episode.video_url;

  return (
    <div className="container mx-auto px-6 py-6">
      <div className="flex items-center gap-3 mb-4 text-sm">
        <Link
          to={`/anime/${id}`}
          className="text-muted hover:text-white transition-colors"
        >
          ← {anime.title}
        </Link>
        <span className="text-muted">/</span>
        <span>Эпизод {episode.number}</span>
      </div>

      <div className="grid lg:grid-cols-[1fr_320px] gap-6">
        <div>
          <div className="glass rounded-2xl overflow-hidden border border-white/5 bg-black">
            {videoSrc.includes("vk.com/video_ext") ||
            videoSrc.includes("vkvideo.ru/video_ext") ? (
            <iframe
                src={videoSrc}
                className="w-full aspect-video bg-black"
                allow="autoplay; encrypted-media; fullscreen; picture-in-picture; screen-wake-lock;"
                allowFullScreen
                frameBorder="0"
            />
            ) : (
            <video
                key={episode.id}
                controls
                autoPlay={false}
                className="w-full aspect-video bg-black"
                poster={episode.thumbnail_url || undefined}
            >
                <source src={videoSrc} type="video/mp4" />
                Ваш браузер не поддерживает видео.
            </video>
            )}
          </div>

          <div className="mt-6">
            <h1 className="text-2xl font-bold font-display">
              {anime.title} — Эпизод {episode.number}
            </h1>
            {episode.title && (
              <p className="text-muted mt-1">{episode.title}</p>
            )}
            {episode.description && (
              <p className="text-gray-300 mt-4 leading-relaxed">
                {episode.description}
              </p>
            )}

            <div className="flex flex-wrap gap-3 mt-6">
              {episode.number > 1 && (
                <Link
                  to={`/watch/${id}/${episode.number - 1}`}
                  className="btn-ghost inline-flex items-center gap-2"
                >
                  ← Предыдущий
                </Link>
              )}
              {episodes.some((e) => e.number === episode.number + 1) && (
                <Link
                  to={`/watch/${id}/${episode.number + 1}`}
                  className="btn-primary inline-flex items-center gap-2"
                >
                  Следующий
                  <ArrowRightIcon className="w-4 h-4" />
                </Link>
              )}
            </div>
          </div>
        </div>

        <aside className="glass rounded-2xl p-4 border border-white/5 h-fit lg:sticky lg:top-20">
          <h3 className="font-bold font-display mb-4">Эпизоды</h3>
          <div className="space-y-1 max-h-[600px] overflow-y-auto">
            {episodes.map((ep) => (
              <Link
                key={ep.id}
                to={`/watch/${id}/${ep.number}`}
                className={`
                  block px-3 py-2.5 rounded-lg text-sm transition-colors
                  ${
                    ep.number === episode.number
                      ? "bg-primary/20 text-primary border border-primary/40"
                      : "text-gray-400 hover:text-white hover:bg-white/5"
                  }
                `}
              >
                <span className="font-medium">Эпизод {ep.number}</span>
                {ep.title && (
                  <span className="block text-xs text-muted mt-0.5 truncate">
                    {ep.title}
                  </span>
                )}
              </Link>
            ))}
          </div>
        </aside>
      </div>
    </div>
  );
}