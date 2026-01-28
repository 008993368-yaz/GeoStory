/**
 * Mock for @arcgis/core modules
 * 
 * This mock is used during tests to avoid loading the heavy ArcGIS library (~2GB).
 * All ArcGIS core modules are aliased to this file in vite.config.ts.
 */

// Mock constructor for all ArcGIS classes
function MockArcGISClass(..._args: unknown[]) {
  return {
    when: () => Promise.resolve(),
    on: () => ({ remove: () => {} }),
    add: () => {},
    remove: () => {},
    destroy: () => {},
    goTo: () => Promise.resolve(),
    toScreen: () => ({ x: 0, y: 0 }),
  };
}

// Default export for Map, MapView, etc.
export default MockArcGISClass;

// Named exports for classes that might be imported as named
export const Map = MockArcGISClass;
export const MapView = MockArcGISClass;
export const GraphicsLayer = MockArcGISClass;
export const Graphic = MockArcGISClass;
export const Point = MockArcGISClass;
export const SimpleMarkerSymbol = MockArcGISClass;
