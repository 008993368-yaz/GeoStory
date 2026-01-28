/**
 * Mock for @arcgis/core/layers/GraphicsLayer
 */

class MockGraphicsLayer {
  constructor(..._args: unknown[]) {
    Object.assign(this, _args[0] || {});
  }
  
  add = () => {};
  remove = () => {};
  removeAll = () => {};
}

export default MockGraphicsLayer;
