import { Link } from "react-router-dom";
import { SettingsIcon } from "./icons";
import type { Profile } from "../types";

interface ProfileHeaderProps {
  profile: Profile;
}

export function ProfileHeader({ profile }: ProfileHeaderProps) {
  const registeredAt = new Date(profile.created_at).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <div className="glass rounded-2xl p-6 md:p-8 border border-white/5">
      <div className="flex flex-col md:flex-row items-start gap-6">
        <div className="w-24 h-24 md:w-28 md:h-28 rounded-3xl bg-gradient-to-br from-primary to-accent flex items-center justify-center text-4xl font-bold text-white flex-shrink-0 shadow-lg shadow-primary/30">
          {profile.avatar_url ? (
            <img
              src={profile.avatar_url}
              alt={profile.username}
              className="w-full h-full rounded-3xl object-cover"
            />
          ) : (
            profile.username[0].toUpperCase()
          )}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold font-display">
                {profile.username}
              </h1>
              <p className="text-muted mt-1">{profile.email}</p>
            </div>

            <Link
              to="/settings"
              className="flex-shrink-0 p-2.5 rounded-xl glass-button hover:bg-primary/25 hover:border-primary/50 transition-all"
              title="Настройки"
            >
              <SettingsIcon className="w-5 h-5" />
            </Link>
          </div>

          {profile.bio && (
            <p className="mt-4 text-gray-300 leading-relaxed">{profile.bio}</p>
          )}

          <div className="flex items-center gap-2 mt-4 text-sm text-muted">
            <span>📅</span>
            <span>Зарегистрирован: {registeredAt}</span>
          </div>
        </div>
      </div>
    </div>
  );
}