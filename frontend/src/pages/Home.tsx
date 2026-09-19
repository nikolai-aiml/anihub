import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export function Home() {
  const { user } = useAuth();

  return (
    <div className="container mx-auto px-4 py-16 text-center">
      <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
        AnimeHub
      </h1>
      <p className="text-xl text-muted mt-6 max-w-2xl mx-auto">
        Твоя личная платформа для аниме: каталог, библиотека, прогресс, оценки и статистика.
      </p>

      <div className="flex justify-center gap-4 mt-10">
        <Link to="/catalog" className="btn-primary">
          Открыть каталог
        </Link>
        {!user && (
          <Link to="/register" className="btn-ghost">
            Создать аккаунт
          </Link>
        )}
      </div>

      <div className="grid md:grid-cols-3 gap-6 mt-20 max-w-4xl mx-auto text-left">
        {[
          { icon: "📚", title: "Каталог", text: "Аниме с жанрами, рейтингами и описаниями" },
          { icon: "📊", title: "Библиотека", text: "Прогресс, оценки, статистика" },
          { icon: "⭐", title: "Достижения", text: "Награды за просмотр и активность" },
        ].map((f) => (
          <div key={f.title} className="card p-6">
            <div className="text-4xl mb-3">{f.icon}</div>
            <h3 className="text-xl font-bold mb-2">{f.title}</h3>
            <p className="text-muted text-sm">{f.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}