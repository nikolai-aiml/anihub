import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "../contexts/AuthContext";
import { useDashboard } from "../hooks/useDashboard";
import { HeroBackground } from "../components/HeroBackground";
import { SakuraPetals } from "../components/SakuraPetals";
import { AmbientParticles } from "../components/AmbientParticles";
import { GlowButton } from "../components/GlowButton";
import { TiltCard } from "../components/TiltCard";
import { AnimeCarousel } from "../components/AnimeCarousel";
import { Loader } from "../components/Loader";
import {
  BookIcon,
  ChartIcon,
  TrophyIcon,
  ArrowRightIcon,
  SparklesIcon,
} from "../components/icons";

const EASE = [0.16, 1, 0.3, 1] as const;

// ============ ГОСТЬ ============
function GuestHome() {
  const features = [
    {
      icon: BookIcon,
      title: "Каталог",
      text: "Тысячи аниме с жанрами, рейтингами и описаниями",
    },
    {
      icon: ChartIcon,
      title: "Библиотека",
      text: "Отслеживай прогресс, ставь оценки, веди статистику",
    },
    {
      icon: TrophyIcon,
      title: "Достижения",
      text: "Получай награды за просмотр и активность",
    },
  ];

  return (
    <div className="relative container mx-auto px-6 py-20 md:py-28" style={{ zIndex: 2 }}>
      <motion.div
        className="text-center"
        initial={{ opacity: 0, y: 30, filter: "blur(12px)" }}
        animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
        transition={{ duration: 0.8, delay: 0.2, ease: EASE }}
      >
        <h1 className="text-6xl md:text-8xl font-bold font-display tracking-tight">
          <span className="title-fill-gradient" data-text="ANIHUB">
            ANIHUB
          </span>
        </h1>

        <p className="text-lg md:text-xl text-gray-400 mt-6 max-w-2xl mx-auto leading-relaxed">
          Твоя личная платформа для аниме: каталог, библиотека, прогресс,
          оценки, статистика
        </p>
      </motion.div>

      <motion.div
        className="flex flex-col sm:flex-row justify-center items-center gap-4 mt-12"
        initial={{ opacity: 0, y: 30, filter: "blur(12px)" }}
        animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
        transition={{ duration: 0.8, delay: 0.4, ease: EASE }}
      >
        <Link to="/catalog">
          <GlowButton variant="primary">
            <BookIcon className="w-5 h-5" />
            Открыть каталог
            <ArrowRightIcon className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" />
          </GlowButton>
        </Link>
        <Link to="/register">
          <GlowButton variant="ghost">
            <SparklesIcon className="w-5 h-5" />
            Создать аккаунт
          </GlowButton>
        </Link>
      </motion.div>

      <div className="grid md:grid-cols-3 gap-6 mt-24 max-w-5xl mx-auto">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 40, filter: "blur(10px)" }}
              animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              transition={{
                duration: 0.7,
                delay: 0.7 + index * 0.15,
                ease: EASE,
              }}
              whileHover={{ y: -8, scale: 1.02 }}
            >
              <TiltCard delay={0}>
                <motion.div
                  className="w-14 h-14 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center mb-6 text-primary"
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  transition={{ duration: 0.3 }}
                >
                  <Icon className="w-7 h-7" />
                </motion.div>

                <h3 className="text-2xl font-bold font-display mb-3 text-white">
                  {feature.title}
                </h3>
                <p className="text-gray-400 leading-relaxed text-sm">
                  {feature.text}
                </p>

                <div className="mt-6 flex items-center gap-2 text-primary text-sm font-medium opacity-0 group-hover:opacity-100 transition-all duration-300 group-hover:translate-x-1">
                  Подробнее
                  <ArrowRightIcon className="w-4 h-4" />
                </div>
              </TiltCard>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

// ============ АВТОРИЗОВАННЫЙ ============
function UserDashboard() {
  const { user } = useAuth();
  const { data: dashboard, isLoading } = useDashboard();

  if (isLoading) return <Loader />;
  if (!dashboard) return null;

  const hasData =
    dashboard.continue_watching.length > 0 ||
    dashboard.recommendations.length > 0;

  return (
    <div className="relative container mx-auto px-6 py-8" style={{ zIndex: 2 }}>
      {/* Приветствие */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: EASE }}
        className="mb-10"
      >
        <h1 className="text-4xl md:text-5xl font-bold font-display">
          С возвращением,{" "}
          <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            {user?.username}
          </span>
        </h1>
        <p className="text-muted mt-2">
          {hasData
            ? "Вот что интересного для вас сегодня"
            : "Начните собирать свою коллекцию аниме"}
        </p>
      </motion.div>

      {/* Продолжить */}
      {dashboard.continue_watching.length > 0 && (
        <AnimeCarousel
          title="📚 Продолжить"
          subtitle="Недавно добавленное в библиотеку"
          anime={dashboard.continue_watching}
          viewAllLink="/library"
        />
      )}

      {/* Рекомендации */}
      {dashboard.recommendations.length > 0 && (
        <AnimeCarousel
          title="✨ Рекомендации для вас"
          subtitle={
            dashboard.top_genres.length > 0
              ? `По вашим любимым жанрам: ${dashboard.top_genres.join(", ")}`
              : "Популярное аниме"
          }
          anime={dashboard.recommendations}
          viewAllLink="/catalog"
        />
      )}

      {/* Популярное */}
      {dashboard.popular.length > 0 && (
        <AnimeCarousel
          title="🔥 Популярное"
          subtitle="Топ по рейтингу"
          anime={dashboard.popular}
          viewAllLink="/catalog?sort=rating"
        />
      )}

      {/* Новые релизы */}
      {dashboard.new_releases.length > 0 && (
        <AnimeCarousel
          title="🆕 Новые релизы"
          subtitle="Последние годы"
          anime={dashboard.new_releases}
          viewAllLink="/catalog?sort=year"
        />
      )}

      {/* Если ничего нет */}
      {!hasData && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-center py-16"
        >
          <div className="text-6xl mb-6">🎬</div>
          <h2 className="text-2xl font-bold font-display mb-3">
            Добро пожаловать в ANIHUB
          </h2>
          <p className="text-muted mb-8 max-w-md mx-auto">
            Откройте каталог, добавьте аниме в библиотеку и получайте
            персональные рекомендации
          </p>
          <Link to="/catalog" className="btn-primary inline-flex items-center gap-2">
            Открыть каталог
            <ArrowRightIcon className="w-4 h-4" />
          </Link>
        </motion.div>
      )}
    </div>
  );
}

// ============ ГЛАВНАЯ ============
export function Home() {
  const { user } = useAuth();

  return (
    <div className="relative min-h-[calc(100vh-4rem)] overflow-hidden">
      <HeroBackground />
      <SakuraPetals />
      <AmbientParticles />

      {user ? <UserDashboard /> : <GuestHome />}
    </div>
  );
}