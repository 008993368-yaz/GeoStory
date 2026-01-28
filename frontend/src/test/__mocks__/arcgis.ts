/**
 * Mock for @arcgis/core modules
 * 
 * Prevents the heavy ArcGIS library from being loaded during tests.
 * Exports stub implementations for all commonly used ArcGIS classes.
 */

export const Map = class {
  destroy() {}
};

export const MapView = class {
  container: HTMLElement | null = null;
  map: unknown = null;
  center: unknown = null;
  zoom: number = 10;
  graphics = {
    removeAll: () => {},
    add: () => {},
  };
  
  destroy() {}
  when() { return Promise.resolve(this); }
  on() { return { remove: () => {} }; }
  goTo() { return Promise.resolve(); }
};

export const GraphicsLayer = class {
  removeAll() {}
  add() {}
};

export const Graphic = class {
  geometry: unknown = null;
  symbol: unknown = null;
  attributes: unknown = null;
};

export const Point = class {
  longitude: number = 0;
  latitude: number = 0;
  constructor(opts?: { longitude?: number; latitude?: number }) {
    if (opts) {
      this.longitude = opts.longitude ?? 0;
      this.latitude = opts.latitude ?? 0;
    }
  }
};

export const SimpleMarkerSymbol = class {
  color: string = 'blue';
  size: string = '10px';
  outline: unknown = null;
};

export const PictureMarkerSymbol = class {
  url: string = '';
  width: string = '24px';
  height: string = '24px';
};

export const TextSymbol = class {
  text: string = '';
  color: string = 'black';
  font: unknown = null;
};

// Default exports for modules that use default exports
export default {
  Map,
  MapView,
  GraphicsLayer,
  Graphic,
  Point,
  SimpleMarkerSymbol,
  PictureMarkerSymbol,
  TextSymbol,
};
