import { Link } from 'react-router-dom';
import { STORY_CATEGORY_LABELS } from '../../constants/story';
import type { StoryRead } from '../../types';

interface StoryCardProps {
  story: StoryRead;
  variant?: 'default' | 'compact';
}

function StoryCard({ story, variant = 'default' }: StoryCardProps) {
  const isCompact = variant === 'compact';
  
  // Format date - prefer date_of_story, fallback to created_at
  const displayDate = story.date_of_story || story.created_at;
  const formattedDate = new Date(displayDate).toLocaleDateString('en-US', {
    year: 'numeric',
    month: isCompact ? 'short' : 'long',
    day: 'numeric',
  });

  // Truncate body for snippet
  const bodySnippet = story.body 
    ? story.body.length > 150 
      ? story.body.substring(0, 150) + '...'
      : story.body
    : 'No content';

  const cardStyle: React.CSSProperties = isCompact
    ? {
        display: 'flex',
        gap: 'var(--spacing-md)',
        border: '1px solid var(--color-border)',
        borderRadius: 'var(--border-radius-md)',
        padding: 'var(--spacing-md)',
        backgroundColor: 'var(--color-background)',
        transition: 'background-color 0.2s ease',
      }
    : {
        border: '1px solid var(--color-border)',
        borderRadius: 'var(--border-radius-lg)',
        padding: 'var(--spacing-lg)',
        backgroundColor: 'var(--color-background)',
        boxShadow: 'var(--shadow-sm)',
        transition: 'box-shadow 0.2s ease, transform 0.2s ease',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
      };

  return (
    <calcite-card
      style={cardStyle}
      onMouseEnter={(e) => {
        if (!isCompact) {
          (e.currentTarget as HTMLElement).style.boxShadow = 'var(--shadow-md)';
          (e.currentTarget as HTMLElement).style.transform = 'translateY(-2px)';
        } else {
          (e.currentTarget as HTMLElement).style.backgroundColor = 'var(--color-surface)';
        }
      }}
      onMouseLeave={(e) => {
        if (!isCompact) {
          (e.currentTarget as HTMLElement).style.boxShadow = 'var(--shadow-sm)';
          (e.currentTarget as HTMLElement).style.transform = 'translateY(0)';
        } else {
          (e.currentTarget as HTMLElement).style.backgroundColor = 'var(--color-background)';
        }
      }}
    >
      <div style={{ flex: 1 }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 'var(--spacing-sm)', marginBottom: 'var(--spacing-sm)' }}>
          <h3 style={{ 
            fontSize: isCompact ? 'var(--font-size-base)' : 'var(--font-size-lg)',
            margin: 0,
            flex: 1,
          }}>
            {story.title}
          </h3>
          {story.category && (
            <calcite-chip
              scale={isCompact ? 's' : 'm'}
              appearance="outline"
              kind="neutral"
            >
              {STORY_CATEGORY_LABELS[story.category] || story.category}
            </calcite-chip>
          )}
        </div>

        {!isCompact && (
          <p
            style={{
              color: 'var(--color-text-secondary)',
              fontSize: 'var(--font-size-sm)',
              marginBottom: 'var(--spacing-md)',
              lineHeight: 'var(--line-height-relaxed)',
            }}
          >
            {bodySnippet}
          </p>
        )}

        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: 'var(--spacing-sm)',
            fontSize: 'var(--font-size-xs)',
            color: 'var(--color-text-secondary)',
            marginBottom: isCompact ? '0' : 'var(--spacing-md)',
          }}
        >
          <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            📅 {formattedDate}
          </span>
          <span>•</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            📍 {story.location_lat.toFixed(4)}, {story.location_lng.toFixed(4)}
          </span>
        </div>
      </div>

      {!isCompact && (
        <div style={{ marginTop: 'auto', paddingTop: 'var(--spacing-md)', borderTop: '1px solid var(--color-border)' }}>
          <Link to={`/stories/${story.id}`} style={{ textDecoration: 'none' }}>
            <calcite-button
              appearance="outline"
              kind="neutral"
              scale="s"
              width="full"
            >
              View Story
            </calcite-button>
          </Link>
        </div>
      )}

      {isCompact && (
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Link to={`/stories/${story.id}`} style={{ textDecoration: 'none' }}>
            <calcite-button
              appearance="transparent"
              kind="neutral"
              scale="s"
              iconEnd="chevron-right"
            >
              View
            </calcite-button>
          </Link>
        </div>
      )}
    </calcite-card>
  );
}

export default StoryCard;
