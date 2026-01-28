/**
 * Story API service
 * 
 * Handles all API interactions for story resources
 */

import apiClient from './api';
import type { StoryCreateRequest, StoryRead } from '../types';

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
 * List all stories with optional pagination
 * 
 * @param skip - Number of records to skip
 * @param limit - Maximum number of records to return
 * @returns Promise resolving to array of stories
 */
export async function listStories(skip = 0, limit = 100): Promise<StoryRead[]> {
  const response = await apiClient.get<StoryRead[]>('/stories', {
    params: { skip, limit },
  });
  return response.data;
}
