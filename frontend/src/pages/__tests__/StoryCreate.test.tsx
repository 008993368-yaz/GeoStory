/**
 * Smoke tests for StoryCreate page
 * 
 * Tests form rendering with mocked API and map components.
 * Note: Calcite web components use shadow DOM, so testing form interactions
 * is limited. These tests focus on verifying the page renders correctly.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen, render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import React from 'react';

// Mock the LocationPickerMap component to avoid ArcGIS dependencies
vi.mock('../../components/map/LocationPickerMap', () => ({
  default: () => React.createElement('div', { 'data-testid': 'location-picker-map' }, 'Location Picker Map (Mock)'),
}));

// Mock the stories service
vi.mock('../../services/stories', () => ({
  createStory: vi.fn(),
}));

// Import StoryCreate - LocationPickerMap will be mocked
import StoryCreate from '../StoryCreate';

// Helper function to render with router
const renderComponent = () => {
  return render(
    <MemoryRouter>
      <StoryCreate />
    </MemoryRouter>
  );
};

describe('StoryCreate page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders page title', () => {
    renderComponent();
    expect(screen.getByText('Create New Story')).toBeInTheDocument();
  });

  it('renders form fields (Title, Latitude, Longitude labels)', () => {
    renderComponent();

    // Check for form labels
    expect(screen.getByText('Title')).toBeInTheDocument();
    expect(screen.getByText('Latitude')).toBeInTheDocument();
    expect(screen.getByText('Longitude')).toBeInTheDocument();
    expect(screen.getByText('Story Content')).toBeInTheDocument();
    expect(screen.getByText('Category')).toBeInTheDocument();
  });

  it('renders Create Story button', () => {
    renderComponent();
    expect(screen.getByText('Create Story')).toBeInTheDocument();
  });

  it('renders Cancel button', () => {
    renderComponent();
    expect(screen.getByText('Cancel')).toBeInTheDocument();
  });

  it('renders mocked LocationPickerMap', () => {
    renderComponent();
    expect(screen.getByTestId('location-picker-map')).toBeInTheDocument();
  });
});
