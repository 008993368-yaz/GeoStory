import { Link } from 'react-router-dom';
import StoryCard from '../components/story/StoryCard';
import type { Story } from '../types';

const mockStories: Story[] = [
  {
    id: '1',
    title: 'My First Story',
    description: 'An example story about geographic data visualization',
    author: 'John Doe',
    createdAt: '2026-01-20T10:00:00Z',
    updatedAt: '2026-01-20T10:00:00Z',
  },
  {
    id: '2',
    title: 'Urban Development Trends',
    description: 'Exploring urban growth patterns across major cities',
    author: 'Jane Smith',
    createdAt: '2026-01-19T14:30:00Z',
    updatedAt: '2026-01-19T14:30:00Z',
  },
];

function Home() {
  return (
    <div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 'var(--spacing-xl)',
        }}
      >
        <h1>GeoStories</h1>
        <Link
          to="/stories/new"
          style={{
            padding: 'var(--spacing-sm) var(--spacing-lg)',
            backgroundColor: 'var(--color-primary)',
            color: 'var(--color-text-on-primary)',
            borderRadius: 'var(--border-radius-md)',
            textDecoration: 'none',
            fontWeight: 'var(--font-weight-medium)',
          }}
        >
          Create Story
        </Link>
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
          gap: 'var(--spacing-lg)',
        }}
      >
        {mockStories.map((story) => (
          <StoryCard key={story.id} story={story} />
        ))}
      </div>
    </div>
  );
}

export default Home;
