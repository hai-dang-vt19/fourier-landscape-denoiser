import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Lắng nghe trên tất cả interfaces (IPv4 và IPv6)
    port: 3000,
    strictPort: false, // Cho phép dùng port khác nếu 3000 bị chiếm
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        ws: true, // Enable websocket proxy
      },
    },
  },
})

