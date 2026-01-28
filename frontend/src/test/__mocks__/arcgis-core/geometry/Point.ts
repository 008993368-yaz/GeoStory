/**
 * Mock for @arcgis/core/geometry/Point
 */

class MockPoint {
  longitude: number = 0;
  latitude: number = 0;
  
  constructor(props?: { longitude?: number; latitude?: number; x?: number; y?: number }) {
    if (props) {
      this.longitude = props.longitude ?? props.x ?? 0;
      this.latitude = props.latitude ?? props.y ?? 0;
    }
  }
}

export default MockPoint;
