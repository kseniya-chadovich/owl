import { defineConfig } from "vite";
import laravel from "laravel-vite-plugin";
import vue from "@vitejs/plugin-vue";

import path from "path";

export default defineConfig({
  plugins: [
    laravel({
            input: ["resources/js/app.js"],
            refresh: true,
        }),
        vue(),
  ],
  resolve: {
    alias: {
        "@": path.resolve(__dirname, "./resources/js"),
        "@components": path.resolve(__dirname, "./resources/js/components"),
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    transformMode: {
      web: [/\.vue$/],
    },
    setupFiles: ["./tests/setup/filter-warnings.js"],
  },
  define: {
    'process.env.VITEST': JSON.stringify(true),
  },
});
