// Story category type matching backend enum
export type StoryCategory = 
  | 'travel'
  | 'food'
  | 'history'
  | 'culture'
  | 'nature'
  | 'urban'
  | 'personal';

// Request payload for creating a story
export interface StoryCreateRequest {
  title: string;
  body?: string | null;
  category?: StoryCategory | null;
  location_lat: number;
  location_lng: number;
  date_of_story?: string | null; // ISO date format "YYYY-MM-DD"
}

// Response from the API when reading a story
export interface StoryRead {
  id: string;
  title: string;
  body?: string | null;
  category?: StoryCategory | null;
  location_lat: number;
  location_lng: number;
  date_of_story?: string | null;
  owner_id?: string | null;
  created_at: string;
  updated_at: string;
  photos: Array<{
    id: string;
    url: string;
    caption?: string | null;
  }>;
}

// Response from list stories endpoint with pagination metadata
export interface StoryListResponse {
  items: StoryRead[];
  total: number;
  limit: number;
  offset: number;
}

// Legacy types (for backward compatibility with existing components)
export interface Story {
  id: string;
  title: string;
  description: string;
  author: string;
  createdAt: string;
  updatedAt: string;
}

export interface StoryCreatePayload {
  title: string;
  description: string;
}
