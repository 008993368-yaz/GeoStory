/**
 * Mock for @arcgis/core/Graphic
 */

class MockGraphic {
  geometry: unknown = null;
  symbol: unknown = null;
  
  constructor(props?: { geometry?: unknown; symbol?: unknown }) {
    if (props) {
      Object.assign(this, props);
    }
  }
}

export default MockGraphic;
