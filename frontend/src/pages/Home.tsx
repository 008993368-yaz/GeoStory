import { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { listStories } from '../services/stories';
import { STORY_CATEGORIES, STORY_CATEGORY_LABELS } from '../constants/story';
import StoryCard from '../components/story/StoryCard';
import MapView from '../components/map/MapView';
import type { StoryRead } from '../types';

type ViewMode = 'list' | 'timeline';

function Home() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  // State
  const [stories, setStories] = useState<StoryRead[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedStoryId, setSelectedStoryId] = useState<string | null>(null);
  
  // Ref for scrolling to selected card
  const selectedCardRefs = useRef<Record<string, HTMLDivElement | null>>({});
  
  // Get initial values from URL params
  const view = (searchParams.get('view') as ViewMode) || 'list';
  const limit = parseInt(searchParams.get('limit') || '20', 10);
  const offset = parseInt(searchParams.get('offset') || '0', 10);
  const category = searchParams.get('category') || '';
  const searchQuery = searchParams.get('q') || '';
  const [searchInput, setSearchInput] = useState(searchQuery);

  // Debounced search effect
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchInput !== searchQuery) {
        updateParam('q', searchInput || null);
        updateParam('offset', '0'); // Reset to first page on search
      }
    }, 300);
    
    return () => clearTimeout(timer);
  }, [searchInput]);

  // Helper to update URL params
  const updateParam = useCallback((key: string, value: string | null) => {
    setSearchParams((prev) => {
      const newParams = new URLSearchParams(prev);
      if (value) {
        newParams.set(key, value);
      } else {
        newParams.delete(key);
      }
      return newParams;
    });
  }, [setSearchParams]);

  // Fetch stories
  const fetchStories = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await listStories({
        limit,
        offset,
        category: category || undefined,
        q: searchQuery || undefined,
        order: view === 'timeline' ? 'desc' : undefined,
      });
      
      setStories(response.items);
      setTotal(response.total);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to load stories. Please try again.';
      setError(errorMessage);
      console.error('Error fetching stories:', err);
    } finally {
      setIsLoading(false);
    }
  }, [limit, offset, category, searchQuery, view]);

  // Fetch on mount and when params change
  useEffect(() => {
    fetchStories();
  }, [fetchStories]);

  // Handlers
  const handleViewChange = (newView: ViewMode) => {
    updateParam('view', newView);
    updateParam('offset', '0'); // Reset pagination
  };

  const handleCategoryChange = (newCategory: string) => {
    updateParam('category', newCategory || null);
    updateParam('offset', '0'); // Reset pagination
  };

  const handlePrevPage = () => {
    const newOffset = Math.max(0, offset - limit);
    updateParam('offset', newOffset.toString());
  };

  const handleNextPage = () => {
    const newOffset = offset + limit;
    if (newOffset < total) {
      updateParam('offset', newOffset.toString());
    }
  };

  const handleSelectStory = (storyId: string) => {
    setSelectedStoryId(storyId);
    
    // Scroll to the selected card if it exists
    setTimeout(() => {
      const cardElement = selectedCardRefs.current[storyId];
      if (cardElement) {
        cardElement.scrollIntoView({
          behavior: 'smooth',
          block: 'nearest',
        });
      }
    }, 100);
  };

  // Computed values
  const currentPage = Math.floor(offset / limit) + 1;
  const totalPages = Math.ceil(total / limit);
  const showingFrom = total > 0 ? offset + 1 : 0;
  const showingTo = Math.min(offset + limit, total);
  const hasPrevPage = offset > 0;
  const hasNextPage = offset + limit < total;

  // Group stories by date for timeline view
  const storiesByDate = useMemo(() => {
    if (view !== 'timeline') return {};
    
    return stories.reduce((acc, story) => {
      const date = story.date_of_story || story.created_at.split('T')[0];
      if (!acc[date]) {
        acc[date] = [];
      }
      acc[date].push(story);
      return acc;
    }, {} as Record<string, StoryRead[]>);
  }, [stories, view]);

  const timelineDates = useMemo(() => {
    return Object.keys(storiesByDate).sort((a, b) => 
      new Date(b).getTime() - new Date(a).getTime()
    );
  }, [storiesByDate]);

  return (
    <div>
      {/* Header */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 'var(--spacing-xl)',
          flexWrap: 'wrap',
          gap: 'var(--spacing-md)',
        }}
      >
        <h1 style={{ margin: 0 }}>GeoStories</h1>
        <Link to="/stories/new" style={{ textDecoration: 'none' }}>
          <calcite-button
            appearance="solid"
            kind="brand"
            scale="m"
            iconStart="plus"
          >
            Create Story
          </calcite-button>
        </Link>
      </div>

      {/* Toolbar */}
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: 'var(--spacing-md)',
          marginBottom: 'var(--spacing-xl)',
          padding: 'var(--spacing-md)',
          backgroundColor: 'var(--color-surface)',
          borderRadius: 'var(--border-radius-md)',
          border: '1px solid var(--color-border)',
        }}
      >
        {/* View Toggle */}
        <div style={{ display: 'flex', gap: 'var(--spacing-xs)' }}>
          <calcite-button
            appearance={view === 'list' ? 'solid' : 'outline'}
            kind={view === 'list' ? 'brand' : 'neutral'}
            scale="s"
            iconStart="grid"
            onClick={() => handleViewChange('list')}
            aria-label="List view"
          >
            List
          </calcite-button>
          <calcite-button
            appearance={view === 'timeline' ? 'solid' : 'outline'}
            kind={view === 'timeline' ? 'brand' : 'neutral'}
            scale="s"
            iconStart="まtime-clock"
            onClick={() => handleViewChange('timeline')}
            aria-label="Timeline view"
          >
            Timeline
          </calcite-button>
        </div>

        {/* Category Filter */}
        <calcite-label layout="inline" scale="s" style={{ flex: '0 0 auto', minWidth: '200px' }}>
          Category
          <calcite-select
            value={category}
            onCalciteSelectChange={(e: any) => handleCategoryChange(e.target.value)}
            scale="s"
            width="full"
          >
            <calcite-option value="" label="All Categories"></calcite-option>
            {STORY_CATEGORIES.map((cat) => (
              <calcite-option 
                key={cat} 
                value={cat} 
                label={STORY_CATEGORY_LABELS[cat]}
              ></calcite-option>
            ))}
          </calcite-select>
        </calcite-label>

        {/* Search */}
        <calcite-label layout="inline" scale="s" style={{ flex: '1 1 200px' }}>
          Search
          <calcite-input
            type="text"
            value={searchInput}
            onCalciteInputInput={(e: any) => setSearchInput(e.target.value)}
            placeholder="Search stories..."
            scale="s"
            clearable
            icon="search"
          />
        </calcite-label>
      </div>

      {/* Map Section */}
      <div style={{ marginBottom: 'var(--spacing-xl)' }}>
        <h2 style={{ 
          fontSize: 'var(--font-size-xl)', 
          marginBottom: 'var(--spacing-md)',
          fontWeight: 600
        }}>
          Map
        </h2>
        <MapView 
          height={400} 
          stories={stories}
          selectedStoryId={selectedStoryId}
          onSelectStory={handleSelectStory}
        />
      </div>

      {/* Error State */}
      {error && (
        <calcite-notice kind="danger" open closable style={{ marginBottom: 'var(--spacing-lg)' }}>
          <div slot="title">Error Loading Stories</div>
          <div slot="message">{error}</div>
          <calcite-button
            slot="actions-end"
            appearance="outline"
            kind="danger"
            scale="s"
            onClick={fetchStories}
          >
            Retry
          </calcite-button>
        </calcite-notice>
      )}

      {/* Loading State */}
      {isLoading && (
        <div style={{ textAlign: 'center', padding: 'var(--spacing-xxl)' }}>
          <calcite-loader scale="l" label="Loading stories..."></calcite-loader>
          <p style={{ marginTop: 'var(--spacing-md)', color: 'var(--color-text-secondary)' }}>
            Loading stories...
          </p>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && !error && stories.length === 0 && (
        <div
          style={{
            textAlign: 'center',
            padding: 'var(--spacing-xxl)',
            backgroundColor: 'var(--color-surface)',
            borderRadius: 'var(--border-radius-lg)',
            border: '2px dashed var(--color-border)',
          }}
        >
          <h2 style={{ fontSize: 'var(--font-size-xl)', marginBottom: 'var(--spacing-md)' }}>
            No Stories Found
          </h2>
          <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--spacing-lg)' }}>
            {searchQuery || category
              ? 'Try adjusting your filters or search terms.'
              : 'Be the first to share your story with the world!'}
          </p>
          <Link to="/stories/new" style={{ textDecoration: 'none' }}>
            <calcite-button
              appearance="solid"
              kind="brand"
              scale="m"
              iconStart="plus"
            >
              Create Your First Story
            </calcite-button>
          </Link>
        </div>
      )}

      {/* List View */}
      {!isLoading && !error && stories.length > 0 && view === 'list' && (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: 'var(--spacing-lg)',
            marginBottom: 'var(--spacing-xl)',
          }}
        >
          {stories.map((story) => (
            <div
              key={story.id}
              ref={(el) => (selectedCardRefs.current[story.id] = el)}
              onClick={() => handleSelectStory(story.id)}
              style={{
                cursor: 'pointer',
                outline: selectedStoryId === story.id ? '2px solid var(--color-primary)' : 'none',
                borderRadius: 'var(--border-radius-md)',
                transition: 'outline 0.2s ease',
              }}
            >
              <StoryCard story={story} variant="default" />
            </div>
          ))}
        </div>
      )}

      {/* Timeline View */}
      {!isLoading && !error && stories.length > 0 && view === 'timeline' && (
        <div style={{ marginBottom: 'var(--spacing-xl)' }}>
          {timelineDates.map((date) => (
            <div key={date} style={{ marginBottom: 'var(--spacing-xl)' }}>
              {/* Date Header */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--spacing-md)',
                  marginBottom: 'var(--spacing-md)',
                }}
              >
                <h2 style={{ 
                  fontSize: 'var(--font-size-lg)',
                  fontWeight: 'var(--font-weight-semibold)',
                  margin: 0,
                  color: 'var(--color-primary)',
                }}>
                  {new Date(date).toLocaleDateString('en-US', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </h2>
                <div style={{ flex: 1, height: '1px', backgroundColor: 'var(--color-border)' }}></div>
              </div>
              
              {/* Stories for this date */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-md)' }}>
                {storiesByDate[date].map((story) => (
                  <div
                    key={story.id}
                    ref={(el) => (selectedCardRefs.current[story.id] = el)}
                    onClick={() => handleSelectStory(story.id)}
                    style={{
                      cursor: 'pointer',
                      outline: selectedStoryId === story.id ? '2px solid var(--color-primary)' : 'none',
                      borderRadius: 'var(--border-radius-md)',
                      transition: 'outline 0.2s ease',
                    }}
                  >
                    <StoryCard story={story} variant="compact" />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {!isLoading && !error && total > 0 && (
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: 'var(--spacing-md)',
            backgroundColor: 'var(--color-surface)',
            borderRadius: 'var(--border-radius-md)',
            border: '1px solid var(--color-border)',
            flexWrap: 'wrap',
            gap: 'var(--spacing-md)',
          }}
        >
          <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)' }}>
            Showing {showingFrom}–{showingTo} of {total} stories
            {totalPages > 1 && ` (Page ${currentPage} of ${totalPages})`}
          </div>
          
          <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
            <calcite-button
              appearance="outline"
              kind="neutral"
              scale="s"
              iconStart="chevron-left"
              onClick={handlePrevPage}
              disabled={!hasPrevPage}
              aria-label="Previous page"
            >
              Previous
            </calcite-button>
            <calcite-button
              appearance="outline"
              kind="neutral"
              scale="s"
              iconEnd="chevron-right"
              onClick={handleNextPage}
              disabled={!hasNextPage}
              aria-label="Next page"
            >
              Next
            </calcite-button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;
