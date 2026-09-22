import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  useNotifications,
  useUnreadCount,
  useNotificationActions,
} from "../hooks/useNotifications";
import type { Notification, NotificationType } from "../types";

const ICONS: Record<NotificationType, string> = {
  achievement: "🏆",
  review_like: "👍",
  library_add: "📚",
  favorite_add: "❤️",
  system: "ℹ️",
};

function timeAgo(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diff = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (diff < 60) return "только что";
  if (diff < 3600) return `${Math.floor(diff / 60)} мин назад`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} ч назад`;
  if (diff < 604800) return `${Math.floor(diff / 86400)} дн назад`;

  return date.toLocaleDateString("ru-RU");
}

export function NotificationsDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const { data: notifications = [] } = useNotifications();
  const { data: unread } = useUnreadCount();
  const { markRead, markAllRead } = useNotificationActions();

  const unreadCount = unread?.count ?? 0;

  // Закрытие при клике вне
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleClick = (n: Notification) => {
    if (!n.is_read) {
      markRead.mutate(n.id);
    }
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Кнопка-колокольчик */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 rounded-lg hover:bg-white/5 transition-colors text-gray-300 hover:text-white"
        aria-label="Уведомления"
      >
        <svg
          className="w-5 h-5"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
          <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
        </svg>

        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 min-w-[18px] h-[18px] px-1 rounded-full bg-accent text-white text-[10px] font-bold flex items-center justify-center">
            {unreadCount > 99 ? "99+" : unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown */}
      {isOpen && (
        <div className="absolute right-0 top-full mt-2 w-80 sm:w-96 z-50 glass-strong rounded-2xl border border-white/10 shadow-2xl overflow-hidden">
          {/* Заголовок */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-white/10">
            <h3 className="font-bold font-display">Уведомления</h3>
            {unreadCount > 0 && (
              <button
                onClick={() => markAllRead.mutate()}
                disabled={markAllRead.isPending}
                className="text-xs text-primary hover:text-primary-hover transition-colors"
              >
                Прочитать все
              </button>
            )}
          </div>

          {/* Список */}
          <div className="max-h-[400px] overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="py-12 text-center text-sm text-muted">
                Нет уведомлений
              </div>
            ) : (
              notifications.map((n) => {
                const icon = ICONS[n.type] || "ℹ️";
                const content = (
                  <div
                    className={`
                      flex gap-3 p-4 border-b border-white/5 hover:bg-white/5 transition-colors cursor-pointer
                      ${!n.is_read ? "bg-primary/5" : ""}
                    `}
                    onClick={() => handleClick(n)}
                  >
                    <div className="text-2xl flex-shrink-0">{icon}</div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start gap-2">
                        <p className="text-sm font-medium text-white">
                          {n.title}
                        </p>
                        {!n.is_read && (
                          <span className="w-2 h-2 rounded-full bg-accent flex-shrink-0 mt-1.5" />
                        )}
                      </div>
                      <p className="text-xs text-gray-400 mt-1 line-clamp-2">
                        {n.message}
                      </p>
                      <p className="text-xs text-muted mt-1">
                        {timeAgo(n.created_at)}
                      </p>
                    </div>
                  </div>
                );

                return n.link ? (
                  <Link key={n.id} to={n.link} onClick={() => handleClick(n)}>
                    {content}
                  </Link>
                ) : (
                  <div key={n.id}>{content}</div>
                );
              })
            )}
          </div>
        </div>
      )}
    </div>
  );
}