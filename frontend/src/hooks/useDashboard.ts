import { useQuery } from "@tanstack/react-query";
import { dashboardApi } from "../api/dashboard";
import { useAuth } from "../contexts/AuthContext";

export function useDashboard() {
  const { user } = useAuth();

  return useQuery({
    queryKey: ["dashboard", user?.id ?? "me"],
    queryFn: () => dashboardApi.get(),
    enabled: !!user,
    staleTime: 5 * 60_000,   // 5 минут
  });
}