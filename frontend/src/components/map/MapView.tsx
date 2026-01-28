/**
 * MapView Component
 * 
 * Renders an ArcGIS map with proper lifecycle management.
 * Handles mount/unmount cleanly to prevent memory leaks.
 */

import { useEffect, useRef, useState } from 'react';
import Map from '@arcgis/core/Map';
import ArcGISMapView from '@arcgis/core/views/MapView';

interface MapViewProps {
  /** Height of the map container (default: 400) */
  height?: string | number;
  /** Center coordinates [longitude, latitude] (default: Los Angeles) */
  center?: [number, number];
  /** Initial zoom level (default: 10) */
  zoom?: number;
}

function MapView({ 
  height = 400, 
  center = [-118.2437, 34.0522],
  zoom = 10 
}: MapViewProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapViewRef = useRef<ArcGISMapView | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Guard: ensure container exists
    if (!mapContainerRef.current) {
      return;
    }

    // Prevent duplicate map instances
    if (mapViewRef.current) {
      return;
    }

    let isMounted = true;

    // Initialize map
    const initMap = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // Create the map
        const map = new Map({
          basemap: 'streets-vector', // Modern vector basemap
        });

        // Create the view
        const view = new ArcGISMapView({
          container: mapContainerRef.current!,
          map: map,
          center: center,
          zoom: zoom,
          // UI options
          popup: {
            dockEnabled: true,
            dockOptions: {
              buttonEnabled: false,
              breakpoint: false,
            },
          },
        });

        // Store view reference for cleanup
        mapViewRef.current = view;

        // Wait for view to be ready
        await view.when();

        if (isMounted) {
          setIsLoading(false);
        }
      } catch (err) {
        console.error('Error initializing map:', err);
        if (isMounted) {
          setError('Failed to load map. Please refresh the page.');
          setIsLoading(false);
        }
      }
    };

    initMap();

    // Cleanup function
    return () => {
      isMounted = false;
      
      // Destroy the view to prevent memory leaks
      if (mapViewRef.current) {
        mapViewRef.current.destroy();
        mapViewRef.current = null;
      }
    };
  }, [center, zoom]); // Re-initialize if center or zoom changes

  // Calculate height style
  const heightStyle = typeof height === 'number' ? `${height}px` : height;

  return (
    <div style={{ position: 'relative', width: '100%', height: heightStyle }}>
      {/* Map Container */}
      <div
        ref={mapContainerRef}
        style={{
          width: '100%',
          height: '100%',
          borderRadius: 'var(--border-radius-md)',
          overflow: 'hidden',
        }}
        aria-label="Interactive map showing story locations"
      />

      {/* Loading Overlay */}
      {isLoading && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: 'var(--color-surface)',
            borderRadius: 'var(--border-radius-md)',
            zIndex: 1,
          }}
        >
          <calcite-loader scale="l" label="Loading map..."></calcite-loader>
          <p style={{ marginTop: 'var(--spacing-md)', color: 'var(--color-text-secondary)' }}>
            Loading map...
          </p>
        </div>
      )}

      {/* Error State */}
      {error && (
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
            backgroundColor: 'var(--color-surface)',
            borderRadius: 'var(--border-radius-md)',
            zIndex: 1,
            padding: 'var(--spacing-lg)',
          }}
        >
          <calcite-notice kind="danger" open width="auto">
            <div slot="title">Map Error</div>
            <div slot="message">{error}</div>
          </calcite-notice>
        </div>
      )}
    </div>
  );
}

export default MapView;
