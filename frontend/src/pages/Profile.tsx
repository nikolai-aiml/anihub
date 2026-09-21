import { useState } from "react";
import { useProfile } from "../hooks/useProfile";
import { ProfileHeader } from "../components/ProfileHeader";
import { ProfileStats } from "../components/ProfileStats";
import { Loader } from "../components/Loader";
import { Library } from "./Library";
import { Favorites } from "./Favorites";

type Tab = "overview" | "library" | "favorites";

const TABS: Array<{ value: Tab; label: string }> = [
  { value: "overview", label: "Обзор" },
  { value: "library", label: "Библиотека" },
  { value: "favorites", label: "Избранное" },
];

export function Profile() {
  const { data: profile, isLoading } = useProfile();
  const [activeTab, setActiveTab] = useState<Tab>("overview");

  if (isLoading) return <Loader />;
  if (!profile) return null;

  return (
    <div className="container mx-auto px-6 py-8">
      <ProfileHeader profile={profile} />

      <div className="mt-8">
        <ProfileStats stats={profile.stats} />
      </div>

      <div className="flex flex-wrap gap-2 mt-8 mb-6">
        {TABS.map((tab) => (
          <button
            key={tab.value}
            onClick={() => setActiveTab(tab.value)}
            className={`
              px-5 py-2.5 rounded-xl text-sm font-medium transition-all
              ${
                activeTab === tab.value
                  ? "bg-primary/20 text-primary border border-primary/40"
                  : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
              }
            `}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div>
        {activeTab === "overview" && (
          <div className="text-center py-12">
            <p className="text-muted">
              Добро пожаловать в твой профиль, {profile.username}!
            </p>
          </div>
        )}

        {activeTab === "library" && <Library />}
        {activeTab === "favorites" && <Favorites />}
      </div>
    </div>
  );
}