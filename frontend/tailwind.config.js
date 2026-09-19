/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0a0a0f",
        surface: "#15151f",
        border: "#25253a",
        primary: "#8b5cf6",
        "primary-hover": "#7c3aed",
        accent: "#ec4899",
        muted: "#71717a",
      },
    },
  },
  plugins: [],
};