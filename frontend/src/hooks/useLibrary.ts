import { useQuery } from "@tanstack/react-query";
import { libraryApi } from "../api/library";
import type { LibraryEntry } from "../types";

export function useLibrary() {
  return useQuery<LibraryEntry[]>({
    queryKey: ["library", "all"],
    queryFn: () => libraryApi.list(),
  });
}

export function useLibraryStats() {
  return useQuery({
    queryKey: ["library", "stats"],
    queryFn: () => libraryApi.stats(),
  });
}