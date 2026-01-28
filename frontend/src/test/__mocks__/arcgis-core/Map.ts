/**
 * Mock for @arcgis/core/Map
 */

class MockMap {
  constructor(..._args: unknown[]) {
    Object.assign(this, _args[0] || {});
  }
}

export default MockMap;
