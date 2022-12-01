import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    hmr: {
      protocol: 'ws',
      host: 'localhost'
    }
  },
  preview: {
    host: true
  },
  build: {
    target: 'esnext',
    minify: false,
    reportCompressedSize: false
  }
})
