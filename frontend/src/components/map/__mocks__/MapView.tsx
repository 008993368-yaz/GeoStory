/**
 * Mock for MapView component
 * 
 * Prevents ArcGIS from being imported during tests.
 */

interface Story {
  id: string;
  title: string;
  category?: string | null;
  location_lat: number;
  location_lng: number;
}

interface Props {
  stories?: Story[];
  selectedStoryId?: string | null;
  onSelectStory?: (id: string) => void;
  height?: string | number;
}

export default function MapView({ stories, onSelectStory }: Props) {
  return (
    <div data-testid="map-view">
      <p>Map with {stories?.length ?? 0} stories</p>
      {stories?.map((story) => (
        <button
          key={story.id}
          onClick={() => onSelectStory?.(story.id)}
          data-testid={`map-pin-${story.id}`}
        >
          {story.title}
        </button>
      ))}
    </div>
  );
}
