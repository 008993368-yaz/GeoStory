/**
 * LocationPickerMap Component
 * 
 * Interactive map for selecting a location by clicking.
 * Displays a marker at the selected position and syncs with external coordinates.
 */

import { useEffect, useRef, useState } from 'react';
import esriConfig from '@arcgis/core/config';
import Map from '@arcgis/core/Map';
import ArcGISMapView from '@arcgis/core/views/MapView';
import GraphicsLayer from '@arcgis/core/layers/GraphicsLayer';
import Graphic from '@arcgis/core/Graphic';
import Point from '@arcgis/core/geometry/Point';
import SimpleMarkerSymbol from '@arcgis/core/symbols/SimpleMarkerSymbol';
import Basemap from '@arcgis/core/Basemap';
import WebTileLayer from '@arcgis/core/layers/WebTileLayer';

// Configure ArcGIS API key if available
const apiKey = import.meta.env.VITE_ARCGIS_API_KEY;
if (apiKey) {
  esriConfig.apiKey = apiKey;
}

// Create a custom basemap using OpenStreetMap tiles (no auth required)
function createOSMBasemap(): Basemap {
  const osmLayer = new WebTileLayer({
    urlTemplate: 'https://tile.openstreetmap.org/{level}/{col}/{row}.png',
    copyright: '© OpenStreetMap contributors',
    subDomains: ['a', 'b', 'c'],
  });
  
  return new Basemap({
    baseLayers: [osmLayer],
    title: 'OpenStreetMap',
    id: 'custom-osm',
  });
}

interface LocationPickerMapProps {
  /** Current location value { lat, lng } or null */
  value?: { lat: number; lng: number } | null;
  /** Callback when location is selected from map */
  onChange: (coords: { lat: number; lng: number }) => void;
  /** Height of map container (default: 320) */
  height?: string | number;
  /** Initial center [longitude, latitude] (default: Los Angeles) */
  center?: [number, number];
  /** Initial zoom level (default: 10) */
  zoom?: number;
}

function LocationPickerMap({
  value = null,
  onChange,
  height = 320,
  center = [-118.2437, 34.0522],
  zoom = 10,
}: LocationPickerMapProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapViewRef = useRef<ArcGISMapView | null>(null);
  const graphicsLayerRef = useRef<GraphicsLayer | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize map and view
  useEffect(() => {
    if (!mapContainerRef.current) return;
    if (mapViewRef.current) return;

    let isMounted = true;
    let clickHandler: any = null;
    let initTimeout: ReturnType<typeof setTimeout>;

    const initMap = async () => {
      // Check if still mounted before creating expensive resources
      if (!isMounted || !mapContainerRef.current) {
        return;
      }

      try {
        setIsLoading(true);
        setError(null);

        // Create graphics layer for location marker
        const graphicsLayer = new GraphicsLayer({
          id: 'location-marker-layer',
        });
        graphicsLayerRef.current = graphicsLayer;

        // Create map with custom OSM basemap (no auth required)
        const map = new Map({
          basemap: createOSMBasemap(),
          layers: [graphicsLayer],
        });

        // Create view
        const view = new ArcGISMapView({
          container: mapContainerRef.current!,
          map: map,
          center: center,
          zoom: zoom,
        });

        mapViewRef.current = view;

        // Handle map clicks to pick location
        clickHandler = view.on('click', (event) => {
          // Get map coordinates from click event
          const mapPoint = view.toMap({ x: event.x, y: event.y });
          
          if (mapPoint && mapPoint.latitude != null && mapPoint.longitude != null) {
            onChange({
              lat: mapPoint.latitude,
              lng: mapPoint.longitude,
            });
          }
        });

        // Wait for view to be ready (ignore AbortError from StrictMode/HMR)
        try {
          await view.when();
        } catch (viewError: any) {
          // AbortError is expected when component unmounts during load
          if (viewError?.name === 'AbortError') {
            return;
          }
          console.warn('Map view warning (may still work):', viewError);
        }

        if (isMounted) {
          setIsLoading(false);
        }
      } catch (err: any) {
        // AbortError is expected during unmount - not a real error
        if (err?.name === 'AbortError') {
          return;
        }
        console.error('Error initializing location picker map:', err);
        if (isMounted) {
          setError(err.message || 'Failed to load map');
          setIsLoading(false);
        }
      }
    };

    // Delay initialization to allow React StrictMode's test unmount to complete
    initTimeout = setTimeout(() => {
      initMap();
    }, 0);

    return () => {
      isMounted = false;
      
      // Clear the timeout if component unmounts before init
      clearTimeout(initTimeout);
      
      if (clickHandler) {
        clickHandler.remove();
      }
      
      if (mapViewRef.current) {
        mapViewRef.current.destroy();
        mapViewRef.current = null;
      }
      
      graphicsLayerRef.current = null;
    };
  }, [center, zoom, onChange]);

  // Update marker when value changes
  useEffect(() => {
    const graphicsLayer = graphicsLayerRef.current;
    if (!graphicsLayer) return;

    // Clear existing marker
    graphicsLayer.removeAll();

    // Add marker if valid coordinates provided
    if (value && isValidCoordinate(value.lat, value.lng)) {
      const point = new Point({
        longitude: value.lng,
        latitude: value.lat,
      });

      const marker = new Graphic({
        geometry: point,
        symbol: new SimpleMarkerSymbol({
          color: [226, 119, 40], // Orange color for selected location
          size: 12,
          outline: {
            color: [255, 255, 255],
            width: 2,
          },
        }),
      });

      graphicsLayer.add(marker);

      // Pan to marker location if view is ready
      if (mapViewRef.current && !mapViewRef.current.updating) {
        mapViewRef.current.goTo({
          target: point,
          zoom: Math.max(mapViewRef.current.zoom, 12),
        }, {
          duration: 500,
        }).catch(() => {
          // Ignore animation errors
        });
      }
    }
  }, [value]);

  // Helper to validate coordinates
  const isValidCoordinate = (lat: number, lng: number): boolean => {
    return (
      typeof lat === 'number' &&
      typeof lng === 'number' &&
      !isNaN(lat) &&
      !isNaN(lng) &&
      lat >= -90 &&
      lat <= 90 &&
      lng >= -180 &&
      lng <= 180
    );
  };

  const heightStyle = typeof height === 'number' ? `${height}px` : height;

  return (
    <div style={{ position: 'relative', width: '100%', height: heightStyle }}>
      {/* Map container */}
      <div
        ref={mapContainerRef}
        style={{
          width: '100%',
          height: '100%',
          borderRadius: 'var(--border-radius-md)',
          overflow: 'hidden',
          cursor: 'crosshair',
        }}
        aria-label="Location picker map - click to select coordinates"
      />

      {/* Loading overlay */}
      {isLoading && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            borderRadius: 'var(--border-radius-md)',
          }}
        >
          <calcite-loader scale="m" label="Loading map..."></calcite-loader>
        </div>
      )}

      {/* Error notice */}
      {error && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '90%',
            maxWidth: '300px',
          }}
        >
          <calcite-notice kind="danger" open icon="exclamation-mark-triangle">
            <div slot="title">Map Error</div>
            <div slot="message">{error}</div>
          </calcite-notice>
        </div>
      )}
    </div>
  );
}

export default LocationPickerMap;
