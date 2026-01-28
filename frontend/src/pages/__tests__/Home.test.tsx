/**
 * Smoke tests for Home page
 * 
 * Tests loading, empty, success, and error states with mocked API.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithRouter } from '../../test/renderWithRouter';

// Mock the stories service - must be before importing Home
vi.mock('../../services/stories', () => ({
  listStories: vi.fn(),
}));

// Mock the MapView component to avoid ArcGIS dependencies - must be before importing Home
vi.mock('../../components/map/MapView', () => ({
  default: ({ stories = [] }: { stories?: unknown[] }) => (
    <div data-testid="map-view">Map with {stories.length} stories</div>
  ),
}));

// Import mocked module after vi.mock calls
import { listStories } from '../../services/stories';
const mockListStories = vi.mocked(listStories);

// Import Home after mocks are set up
import Home from '../Home';

describe('Home page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', async () => {
    // Keep the promise pending to see loading state
    mockListStories.mockImplementation(() => new Promise(() => {}));
    
    renderWithRouter(<Home />);
    
    // Should show loading indicator
    expect(screen.getByText('Loading stories...')).toBeInTheDocument();
  });

  it('renders empty state CTA when API returns no stories', async () => {
    mockListStories.mockResolvedValue({
      items: [],
      total: 0,
      limit: 20,
      offset: 0,
    });

    renderWithRouter(<Home />);

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading stories...')).not.toBeInTheDocument();
    });

    // Should show empty state
    expect(screen.getByText('No Stories Found')).toBeInTheDocument();
    expect(screen.getByText('Create Your First Story')).toBeInTheDocument();
  });

  it('renders story card when API returns stories', async () => {
    const mockStory = {
      id: '123e4567-e89b-12d3-a456-426614174000',
      title: 'My Amazing Adventure',
      body: 'This is the story body',
      category: 'travel' as const,
      location_lat: 34.0522,
      location_lng: -118.2437,
      date_of_story: '2026-01-15',
      owner_id: null,
      created_at: '2026-01-15T10:00:00Z',
      updated_at: '2026-01-15T10:00:00Z',
      photos: [],
    };

    mockListStories.mockResolvedValue({
      items: [mockStory],
      total: 1,
      limit: 20,
      offset: 0,
    });

    renderWithRouter(<Home />);

    // Wait for loading to complete and story to appear
    await waitFor(() => {
      expect(screen.getByText('My Amazing Adventure')).toBeInTheDocument();
    });
  });

  it('renders error notice with Retry button when API fails', async () => {
    const user = userEvent.setup();
    
    // First call fails
    mockListStories.mockRejectedValueOnce(new Error('Network error'));
    
    // Second call (retry) succeeds
    mockListStories.mockResolvedValue({
      items: [],
      total: 0,
      limit: 20,
      offset: 0,
    });

    renderWithRouter(<Home />);

    // Wait for error state
    await waitFor(() => {
      expect(screen.getByText('Error Loading Stories')).toBeInTheDocument();
    });

    // Should show retry button
    const retryButton = screen.getByText('Retry');
    expect(retryButton).toBeInTheDocument();

    // Click retry
    await user.click(retryButton);

    // Should call listStories again
    await waitFor(() => {
      expect(mockListStories).toHaveBeenCalledTimes(2);
    });
  });
});
