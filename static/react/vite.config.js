import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
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
