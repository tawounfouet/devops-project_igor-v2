import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 4173,
    strictPort: true,
    watch: {
      usePolling: true, // Nécessaire pour Docker sur certains systèmes
      interval: 1000,   // Intervalle de polling pour les changements
    },
    hmr: {
      port: 4173,
      host: '0.0.0.0'
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})
