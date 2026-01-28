/**
 * Mock for @arcgis/core
 * 
 * This mock is used during tests to avoid loading the heavy ArcGIS library (~2GB).
 * All @arcgis/core imports will be redirected here via Vite alias.
 */

// Mock class that works as both constructor and object
class MockArcGISClass {
  constructor(..._args: unknown[]) {
    // Store any passed args as properties
    Object.assign(this, _args[0] || {});
  }
  
  when = () => Promise.resolve(this);
  on = () => ({ remove: () => {} });
  add = () => {};
  remove = () => {};
  destroy = () => {};
  goTo = () => Promise.resolve();
  toScreen = () => ({ x: 0, y: 0 });
}

// Main exports
export const Map = MockArcGISClass;
export default MockArcGISClass;
