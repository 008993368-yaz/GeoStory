/**
 * Mock for @arcgis/core/symbols/SimpleMarkerSymbol
 */

class MockSimpleMarkerSymbol {
  color: string = '#000000';
  size: number = 12;
  outline: unknown = null;
  
  constructor(props?: { color?: string; size?: number; outline?: unknown }) {
    if (props) {
      Object.assign(this, props);
    }
  }
}

export default MockSimpleMarkerSymbol;
