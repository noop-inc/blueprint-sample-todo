import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8080,
    hmr: {
      protocol: 'ws',
      host: 'localhost',
      port: 8080
    }
  },
  preview: {
    host: true,
    port: 5000
  }
})
