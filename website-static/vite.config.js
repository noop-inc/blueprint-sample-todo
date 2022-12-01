import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
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
