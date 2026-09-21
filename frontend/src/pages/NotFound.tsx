import { Link } from "react-router-dom";

export function NotFound() {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-6">
      <div className="text-center">
        <h1 className="text-8xl font-bold font-display bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
          404
        </h1>
        <p className="text-2xl font-bold mt-6">Страница не найдена</p>
        <p className="text-muted mt-2">Похоже, этот путь ведёт в никуда.</p>
        <Link
          to="/"
          className="inline-block mt-8 px-6 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold hover:scale-105 transition-transform"
        >
          Вернуться на главную
        </Link>
      </div>
    </div>
  );
}