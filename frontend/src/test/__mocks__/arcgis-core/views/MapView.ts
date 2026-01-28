/**
 * Mock for @arcgis/core/views/MapView
 */

class MockMapView {
  container: HTMLDivElement | null = null;
  
  constructor(props?: { container?: HTMLDivElement; map?: unknown; center?: number[]; zoom?: number }) {
    if (props) {
      Object.assign(this, props);
    }
  }
  
  when = () => Promise.resolve(this);
  on = () => ({ remove: () => {} });
  goTo = () => Promise.resolve();
  toScreen = () => ({ x: 0, y: 0 });
  destroy = () => {};
}

export default MockMapView;
