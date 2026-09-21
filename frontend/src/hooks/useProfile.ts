import { useQuery } from "@tanstack/react-query";
import { profileApi } from "../api/profile";
import { useAuth } from "../contexts/AuthContext";

export function useProfile() {
  const { user } = useAuth();

  return useQuery({
    queryKey: ["profile", user?.id ?? "me"],
    queryFn: () => profileApi.getMe(),
    enabled: !!user,
  });
}