import { NavLink } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import {
  HomeIcon,
  CompassIcon,
  BookIcon,
  HeartIcon,
  TrophyIcon,
  ChartIcon,
  SettingsIcon,
  SearchIcon,
  LockIcon,
} from "./icons";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const { user } = useAuth();

  const navItems = [
    { to: "/", label: "Главная", icon: HomeIcon },
    { to: "/catalog", label: "Каталог", icon: CompassIcon },
    { to: "/search", label: "Поиск", icon: SearchIcon },
    { to: "/library", label: "Библиотека", icon: BookIcon },
    { to: "/favorites", label: "Избранное", icon: HeartIcon },
    { to: "/achievements", label: "Достижения", icon: TrophyIcon },
    { to: "/statistics", label: "Статистика", icon: ChartIcon },
    { to: "/settings", label: "Настройки", icon: SettingsIcon },
  ];

  // Добавляем админку только для суперпользователя
  const items = user?.is_superuser
    ? [...navItems, { to: "/admin", label: "Админ-панель", icon: LockIcon }]
    : navItems;

  return (
    <>
      {/* Оверлей на мобильном */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-16 left-0 bottom-0 w-64 z-40
          glass-strong border-r border-white/5
          transition-transform duration-300
          ${isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
        `}
      >
        <nav className="p-4 space-y-1 overflow-y-auto h-full pb-20">
          {items.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={onClose}
                end={item.to === "/"}
                className={({ isActive }) =>
                  `group flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300 ${
                    isActive
                      ? "bg-primary/15 text-primary border border-primary/30 shadow-lg shadow-primary/10"
                      : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
                  }`
                }
              >
                <Icon className="w-5 h-5 group-hover:scale-110 transition-transform" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* Подвал sidebar */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-white/5 glass-strong">
          <p className="text-xs text-muted text-center">ANIHUB © 2026</p>
        </div>
      </aside>
    </>
  );
}