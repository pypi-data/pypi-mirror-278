import { defineConfig } from "astro/config";
import wasm from "vite-plugin-wasm";

// https://astro.build/config
export default defineConfig({
  srcDir: "frontend",
  vite: {
    optimizeDeps: {
      entries: ["layouts", "pages", "components"],
    },
    plugins: [wasm()],
  },
});
