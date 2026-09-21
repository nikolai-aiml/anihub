import { useQuery } from "@tanstack/react-query";
import { achievementsApi } from "../api/achievements";
import { useAuth } from "../contexts/AuthContext";

export function useAchievements() {
  const { user } = useAuth();

  return useQuery({
    queryKey: ["achievements", user?.id ?? "me"],
    queryFn: () => achievementsApi.list(),
    enabled: !!user,
  });
}