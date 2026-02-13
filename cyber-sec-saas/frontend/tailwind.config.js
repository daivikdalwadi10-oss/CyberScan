/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        navy: "#0f172a",
        slate: "#111827",
        accent: "#3b82f6",
        emerald: "#10b981",
        warning: "#f59e0b",
        critical: "#ef4444"
      },
      fontFamily: {
        display: ["Space Grotesk", "Sora", "sans-serif"],
        body: ["Sora", "Space Grotesk", "sans-serif"]
      }
    }
  },
  plugins: []
};
