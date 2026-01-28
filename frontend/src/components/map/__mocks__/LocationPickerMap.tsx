/**
 * Mock for LocationPickerMap component
 * 
 * Prevents ArcGIS from being imported during tests.
 */

interface Props {
  value?: { lat: number; lng: number } | null;
  onChange?: (coords: { lat: number; lng: number }) => void;
  height?: string | number;
  center?: [number, number];
  zoom?: number;
}

export default function LocationPickerMap({ onChange }: Props) {
  return (
    <div data-testid="location-picker-map">
      <button
        type="button"
        onClick={() => onChange?.({ lat: 34.0522, lng: -118.2437 })}
        data-testid="mock-location-select"
      >
        Mock Location Picker
      </button>
    </div>
  );
}
