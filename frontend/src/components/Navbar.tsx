import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="border-b border-border bg-surface/50 backdrop-blur sticky top-0 z-10">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link
          to="/"
          className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent"
        >
          AnimeHub
        </Link>

        <div className="flex items-center gap-6">
          <Link
            to="/catalog"
            className="text-sm hover:text-primary transition-colors"
          >
            Каталог
          </Link>
          {user ? (
            <>
              <Link
                to="/profile"
                className="text-sm hover:text-primary transition-colors"
              >
                {user.username}
              </Link>
              <button
                onClick={handleLogout}
                className="text-sm text-muted hover:text-white transition-colors"
              >
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="text-sm hover:text-primary transition-colors"
              >
                Войти
              </Link>
              <Link to="/register" className="btn-primary text-sm">
                Регистрация
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}