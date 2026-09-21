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
        fontFamily: {
          sans: ["Inter", "system-ui", "sans-serif"],
          display: ["Space Grotesk", "system-ui", "sans-serif"],
        },
        animation: {
          "fade-up": "fadeUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) both",
          "fade-up-slow": "fadeUp 1s cubic-bezier(0.16, 1, 0.3, 1) both",
          "float": "float 6s ease-in-out infinite",
          "glow-pulse": "glowPulse 3s ease-in-out infinite",
          "arrow-slide": "arrowSlide 1.5s ease-in-out infinite",
          "gradient-shift": "gradientShift 6s ease infinite",
        },
        keyframes: {
          fadeUp: {
            "0%": { opacity: "0", transform: "translateY(20px)", filter: "blur(12px)" },
            "100%": { opacity: "1", transform: "translateY(0)", filter: "blur(0)" },
          },
          float: {
            "0%, 100%": { transform: "translateY(0)" },
            "50%": { transform: "translateY(-8px)" },
          },
          glowPulse: {
            "0%, 100%": { opacity: "0.5" },
            "50%": { opacity: "1" },
          },
          arrowSlide: {
            "0%, 100%": { transform: "translateX(0)" },
            "50%": { transform: "translateX(4px)" },
          },
          gradientShift: {
            "0%, 100%": { backgroundPosition: "0% 50%" },
            "50%": { backgroundPosition: "100% 50%" },
          },
        },
      },
    },
  plugins: [],
};