/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    globals: true,
    testTimeout: 30000,
    pool: 'forks',
    // Alias all ArcGIS imports to lightweight mocks
    // Note: Component mocking is done via vi.mock in test files
    alias: [
      // Mock ArcGIS core modules
      { find: '@arcgis/core/Map', replacement: path.resolve(__dirname, 'src/test/__mocks__/arcgis-core/Map.ts') },
      { find: '@arcgis/core/views/MapView', replacement: path.resolve(__dirname, 'src/test/__mocks__/arcgis-core/views/MapView.ts') },
      { find: '@arcgis/core/layers/GraphicsLayer', replacement: path.resolve(__dirname, 'src/test/__mocks__/arcgis-core/layers/GraphicsLayer.ts') },
      { find: '@arcgis/core/Graphic', replacement: path.resolve(__dirname, 'src/test/__mocks__/arcgis-core/Graphic.ts') },
      { find: '@arcgis/core/geometry/Point', replacement: path.resolve(__dirname, 'src/test/__mocks__/arcgis-core/geometry/Point.ts') },
      { find: '@arcgis/core/symbols/SimpleMarkerSymbol', replacement: path.resolve(__dirname, 'src/test/__mocks__/arcgis-core/symbols/SimpleMarkerSymbol.ts') },
    ],
  },
});
