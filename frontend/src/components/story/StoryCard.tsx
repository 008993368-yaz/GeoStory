import type { Story } from '../../types';

interface StoryCardProps {
  story: Story;
}

function StoryCard({ story }: StoryCardProps) {
  const formattedDate = new Date(story.createdAt).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div
      style={{
        border: '1px solid var(--color-border)',
        borderRadius: 'var(--border-radius-lg)',
        padding: 'var(--spacing-lg)',
        backgroundColor: 'var(--color-background)',
        boxShadow: 'var(--shadow-sm)',
        transition: 'box-shadow 0.2s ease, transform 0.2s ease',
        cursor: 'pointer',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.boxShadow = 'var(--shadow-md)';
        e.currentTarget.style.transform = 'translateY(-2px)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
        e.currentTarget.style.transform = 'translateY(0)';
      }}
    >
      <h3 style={{ marginBottom: 'var(--spacing-sm)' }}>{story.title}</h3>
      <p
        style={{
          color: 'var(--color-text-secondary)',
          fontSize: 'var(--font-size-sm)',
          marginBottom: 'var(--spacing-md)',
        }}
      >
        {story.description}
      </p>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          fontSize: 'var(--font-size-xs)',
          color: 'var(--color-text-secondary)',
          paddingTop: 'var(--spacing-md)',
          borderTop: '1px solid var(--color-border)',
        }}
      >
        <span>{story.author}</span>
        <span>{formattedDate}</span>
      </div>
    </div>
  );
}

export default StoryCard;
