/**
 * Story API service
 * 
 * Handles all API interactions for story resources
 */

import apiClient from './api';
import type { StoryCreateRequest, StoryRead, StoryListResponse } from '../types';

/**
 * Parameters for listing stories
 */
export interface ListStoriesParams {
  limit?: number;
  offset?: number;
  category?: string;
  date_from?: string;
  date_to?: string;
  q?: string;
  order?: 'asc' | 'desc';
}

/**
 * Create a new story
 * 
 * @param payload - Story creation data
 * @returns Promise resolving to the created story
 */
export async function createStory(payload: StoryCreateRequest): Promise<StoryRead> {
  const response = await apiClient.post<StoryRead>('/stories', payload);
  return response.data;
}

/**
 * Get a story by ID
 * 
 * @param id - Story UUID
 * @returns Promise resolving to the story
 */
export async function getStory(id: string): Promise<StoryRead> {
  const response = await apiClient.get<StoryRead>(`/stories/${id}`);
  return response.data;
}

/**
 * List stories with filtering and pagination
 * 
 * @param params - Query parameters for filtering and pagination
 * @returns Promise resolving to paginated story list with metadata
 */
export async function listStories(params: ListStoriesParams = {}): Promise<StoryListResponse> {
  const response = await apiClient.get<StoryListResponse>('/stories', {
    params: {
      limit: params.limit ?? 20,
      offset: params.offset ?? 0,
      ...(params.category && { category: params.category }),
      ...(params.date_from && { date_from: params.date_from }),
      ...(params.date_to && { date_to: params.date_to }),
      ...(params.q && { q: params.q }),
      ...(params.order && { order: params.order }),
    },
  });
  return response.data;
}
