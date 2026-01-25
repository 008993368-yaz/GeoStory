import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../services/api';
import type { StoryCreatePayload } from '../types';

function StoryCreate() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<StoryCreatePayload>({
    title: '',
    description: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      await apiClient.post('/stories', formData);
      navigate('/');
    } catch (err) {
      setError('Failed to create story. Please try again.');
      console.error('Error creating story:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px' }}>
      <h1>Create New Story</h1>

      {error && (
        <div
          style={{
            padding: 'var(--spacing-md)',
            backgroundColor: '#fee',
            color: 'var(--color-error)',
            borderRadius: 'var(--border-radius-md)',
            marginBottom: 'var(--spacing-lg)',
          }}
        >
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 'var(--spacing-lg)' }}>
          <label
            htmlFor="title"
            style={{
              display: 'block',
              marginBottom: 'var(--spacing-sm)',
              fontWeight: 'var(--font-weight-medium)',
            }}
          >
            Title
          </label>
          <input
            type="text"
            id="title"
            value={formData.title}
            onChange={(e) =>
              setFormData({ ...formData, title: e.target.value })
            }
            required
            style={{
              width: '100%',
              padding: 'var(--spacing-sm) var(--spacing-md)',
              border: '1px solid var(--color-border)',
              borderRadius: 'var(--border-radius-md)',
              fontSize: 'var(--font-size-base)',
            }}
          />
        </div>

        <div style={{ marginBottom: 'var(--spacing-lg)' }}>
          <label
            htmlFor="description"
            style={{
              display: 'block',
              marginBottom: 'var(--spacing-sm)',
              fontWeight: 'var(--font-weight-medium)',
            }}
          >
            Description
          </label>
          <textarea
            id="description"
            value={formData.description}
            onChange={(e) =>
              setFormData({ ...formData, description: e.target.value })
            }
            required
            rows={5}
            style={{
              width: '100%',
              padding: 'var(--spacing-sm) var(--spacing-md)',
              border: '1px solid var(--color-border)',
              borderRadius: 'var(--border-radius-md)',
              fontSize: 'var(--font-size-base)',
              resize: 'vertical',
            }}
          />
        </div>

        <div style={{ display: 'flex', gap: 'var(--spacing-md)' }}>
          <button
            type="submit"
            disabled={isSubmitting}
            style={{
              padding: 'var(--spacing-sm) var(--spacing-lg)',
              backgroundColor: 'var(--color-primary)',
              color: 'var(--color-text-on-primary)',
              border: 'none',
              borderRadius: 'var(--border-radius-md)',
              fontWeight: 'var(--font-weight-medium)',
              opacity: isSubmitting ? 0.6 : 1,
            }}
          >
            {isSubmitting ? 'Creating...' : 'Create Story'}
          </button>

          <button
            type="button"
            onClick={() => navigate('/')}
            style={{
              padding: 'var(--spacing-sm) var(--spacing-lg)',
              backgroundColor: 'transparent',
              color: 'var(--color-text-secondary)',
              border: '1px solid var(--color-border)',
              borderRadius: 'var(--border-radius-md)',
              fontWeight: 'var(--font-weight-medium)',
            }}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default StoryCreate;
