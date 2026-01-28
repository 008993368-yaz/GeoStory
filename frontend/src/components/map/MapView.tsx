/**
 * MapView Component
 * 
 * Renders an ArcGIS map with proper lifecycle management.
 * Handles mount/unmount cleanly to prevent memory leaks.
 */

import { useEffect, useRef, useState } from 'react';
import Map from '@arcgis/core/Map';
import ArcGISMapView from '@arcgis/core/views/MapView';
import GraphicsLayer from '@arcgis/core/layers/GraphicsLayer';
import Graphic from '@arcgis/core/Graphic';
import Point from '@arcgis/core/geometry/Point';
import SimpleMarkerSymbol from '@arcgis/core/symbols/SimpleMarkerSymbol';

interface Story {
  id: string;
  title: string;
  category?: string | null;
  location_lat: number;
  location_lng: number;
}

interface MapViewProps {
  /** Height of the map container (default: 400) */
  height?: string | number;
  /** Center coordinates [longitude, latitude] (default: Los Angeles) */
  center?: [number, number];
  /** Initial zoom level (default: 10) */
  zoom?: number;
  /** Array of stories to display as pins */
  stories?: Story[];
  /** Currently selected story ID */
  selectedStoryId?: string | null;
  /** Callback when a story pin is clicked */
  onSelectStory?: (id: string) => void;
}

// Category colors for pins
const CATEGORY_COLORS: Record<string, string> = {
  travel: '#0079c1',
  food: '#d83020',
  history: '#6f4c3e',
  culture: '#9c27b0',
  nature: '#2e7d32',
  urban: '#424242',
  personal: '#f57c00',
};

function MapView({ 
  height = 400, 
  center = [-118.2437, 34.0522],
  zoom = 10,
  stories = [],
  selectedStoryId = null,
  onSelectStory,
}: MapViewProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapViewRef = useRef<ArcGISMapView | null>(null);
  const graphicsLayerRef = useRef<GraphicsLayer | null>(null);
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
    let clickHandler: any = null;

    // Initialize map
    const initMap = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // Create graphics layer for story pins
        const graphicsLayer = new GraphicsLayer({
          id: 'stories-layer',
          title: 'Stories',
        });
        graphicsLayerRef.current = graphicsLayer;

        // Create the map
        const map = new Map({
          basemap: 'streets-vector',
          layers: [graphicsLayer],
        });

        // Create the view
        const view = new ArcGISMapView({
          container: mapContainerRef.current!,
          map: map,
          center: center,
          zoom: zoom,
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

        // Handle pin clicks
        clickHandler = view.on('click', async (event) => {
          try {
            const response = await view.hitTest(event);
            
            // Find if we clicked on a story graphic
            const graphicHit = response.results.find(
              (r: any) => r.type === 'graphic' && r.graphic.layer?.id === 'stories-layer'
            );

            if (graphicHit && onSelectStory) {
              const storyId = (graphicHit as any).graphic.attributes.id;
              onSelectStory(storyId);
            }
          } catch (err) {
            console.error('Error handling map click:', err);
          }
        });

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
      
      // Remove click handler
      if (clickHandler) {
        clickHandler.remove();
      }
      
      // Destroy the view to prevent memory leaks
      if (mapViewRef.current) {
        mapViewRef.current.destroy();
        mapViewRef.current = null;
      }
      
      // Clear graphics layer ref
      graphicsLayerRef.current = null;
    };
  }, [center, zoom, onSelectStory]);

  // Update graphics when stories or selection changes
  useEffect(() => {
    const graphicsLayer = graphicsLayerRef.current;
    if (!graphicsLayer) return;

    // Clear existing graphics
    graphicsLayer.removeAll();

    // Add graphics for each story that has location data
    const graphics = stories
      .filter((story) => story.location_lat && story.location_lng)
      .map((story) => {
        const isSelected = story.id === selectedStoryId;
        const color = story.category ? CATEGORY_COLORS[story.category] || '#0079c1' : '#0079c1';

        const point = new Point({
          longitude: story.location_lng,
          latitude: story.location_lat,
        });

        // Create symbol with highlight for selected story
        const symbol = new SimpleMarkerSymbol({
          color: color,
          size: isSelected ? 14 : 10,
          outline: {
            color: isSelected ? '#ffffff' : color,
            width: isSelected ? 3 : 1,
          },
        });

        return new Graphic({
          geometry: point,
          symbol: symbol,
          attributes: {
            id: story.id,
            title: story.title,
            category: story.category,
          },
          popupTemplate: {
            title: '{title}',
            content: story.category ? `Category: ${story.category}` : 'No category',
          },
        });
      });

    graphicsLayer.addMany(graphics);

    // Pan to selected story if exists
    if (selectedStoryId && mapViewRef.current) {
      const selectedStory = stories.find((s) => s.id === selectedStoryId);
      if (selectedStory && selectedStory.location_lat && selectedStory.location_lng) {
        const point = new Point({
          longitude: selectedStory.location_lng,
          latitude: selectedStory.location_lat,
        });
        
        // Smoothly pan to the selected pin
        mapViewRef.current.goTo(
          {
            target: point,
            zoom: Math.max(mapViewRef.current.zoom, 12), // Zoom in if needed
          },
          {
            duration: 500,
          }
        ).catch((err) => {
          // Ignore goTo errors (e.g., if animation is interrupted)
          console.debug('GoTo animation cancelled or failed:', err);
        });
      }
    }
  }, [stories, selectedStoryId]);

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
