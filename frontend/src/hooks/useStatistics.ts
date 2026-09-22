import { useQuery } from "@tanstack/react-query";
import { statisticsApi } from "../api/statistics";
import { useAuth } from "../contexts/AuthContext";

export function useStatistics() {
  const { user } = useAuth();

  return useQuery({
    queryKey: ["statistics", user?.id ?? "me"],
    queryFn: () => statisticsApi.getMe(),
    enabled: !!user,
  });
}