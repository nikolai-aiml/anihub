import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "../contexts/AuthContext";
import { HeroBackground } from "../components/HeroBackground";
import { GlowButton } from "../components/GlowButton";
import { TiltCard } from "../components/TiltCard";
import {
  BookIcon,
  ChartIcon,
  TrophyIcon,
  ArrowRightIcon,
  SparklesIcon,
} from "../components/icons";

const EASE = [0.16, 1, 0.3, 1] as const;

export function Home() {
  const { user } = useAuth();

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
    <div className="relative min-h-[calc(100vh-4rem)] overflow-hidden">
      {/* Фон */}
      <HeroBackground />

      {/* Контент */}
      <div className="relative container mx-auto px-6 py-20 md:py-28">
        {/* Заголовок */}
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

        {/* Кнопки */}
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

          {!user && (
            <Link to="/register">
              <GlowButton variant="ghost">
                <SparklesIcon className="w-5 h-5" />
                Создать аккаунт
              </GlowButton>
            </Link>
          )}
        </motion.div>

        {/* Карточки */}
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
                  {/* Иконка */}
                  <motion.div
                    className="w-14 h-14 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center mb-6 text-primary"
                    whileHover={{ scale: 1.1, rotate: 5 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Icon className="w-7 h-7" />
                  </motion.div>

                  {/* Заголовок */}
                  <h3 className="text-2xl font-bold font-display mb-3 text-white">
                    {feature.title}
                  </h3>

                  {/* Описание */}
                  <p className="text-gray-400 leading-relaxed text-sm">
                    {feature.text}
                  </p>

                  {/* Стрелка при hover */}
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
    </div>
  );
}