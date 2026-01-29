import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vitePluginImporter from 'vite-plugin-importer'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vitePluginImporter({
      libraryName: 'ant-design-vue',
      libraryDirectory: 'es',
      style: true
    })
  ],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
