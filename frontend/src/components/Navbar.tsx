import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { MenuIcon } from "./icons";
import { NotificationsDropdown } from "./NotificationsDropdown";

interface NavbarProps {
  onMenuClick?: () => void;
}

export function Navbar({ onMenuClick }: NavbarProps) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="sticky top-0 z-50 glass border-b border-white/5">
      <div className="px-4 lg:px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* Кнопка меню — только для авторизованных на мобильном */}
          {user && onMenuClick && (
            <button
              onClick={onMenuClick}
              className="lg:hidden p-2 rounded-lg hover:bg-white/5 transition-colors text-gray-300"
              aria-label="Открыть меню"
            >
              <MenuIcon />
            </button>
          )}

          {/* Логотип */}
          <Link
            to="/"
            className="text-2xl font-bold font-display bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent animate-gradient-shift bg-[length:200%_100%]"
          >
            ANIHUB
          </Link>
        </div>

        {/* Правый блок */}
        <div className="flex items-center gap-2">
          {user ? (
            <>
              {/* Уведомления */}
                  
          <NotificationsDropdown />

              {/* Профиль */}
              <Link
                to="/profile"
                className="flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-white/5 transition-colors"
              >
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-sm font-bold text-white">
                  {user.username[0].toUpperCase()}
                </div>
                <span className="hidden md:block text-sm font-medium text-white">
                  {user.username}
                </span>
              </Link>

              {/* Выйти */}
              <button
                onClick={handleLogout}
                className="hidden md:block px-4 py-2 text-sm font-medium text-muted hover:text-white rounded-lg hover:bg-white/5 transition-all"
              >
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white rounded-lg hover:bg-white/5 transition-all"
              >
                Войти
              </Link>
              <Link
                to="/register"
                className="px-5 py-2 text-sm font-semibold text-white rounded-xl glass-button hover:bg-primary/25 hover:border-primary/50 hover:shadow-lg hover:shadow-primary/20 transition-all"
              >
                Регистрация
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}