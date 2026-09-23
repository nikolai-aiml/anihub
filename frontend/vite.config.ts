import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    watch: {
      // Исключаем видео и другие большие файлы из отслеживания
      ignored: [
        "**/public/videos/**",
        "**/public/posters/**",
        "**/*.mp4",
        "**/*.webm",
        "**/*.mkv",
      ],
    },
    hmr: {
      overlay: false,   // на всякий случай — не блокирует экран при ошибках
    },
  },
});