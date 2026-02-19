import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/pantry": "http://localhost:8000",
      "/preferences": "http://localhost:8000",
      "/recipes": "http://localhost:8000",
      "/vision": "http://localhost:8000",
      "/kb": "http://localhost:8000",
      "/healthz": "http://localhost:8000",
    },
  },
});
