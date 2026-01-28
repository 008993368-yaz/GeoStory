/**
 * Story-related constants
 * 
 * These values should match the backend StoryCategory enum
 */

export const STORY_CATEGORIES = [
  'travel',
  'food',
  'history',
  'culture',
  'nature',
  'urban',
  'personal',
] as const;

export const STORY_CATEGORY_LABELS: Record<string, string> = {
  travel: 'Travel',
  food: 'Food',
  history: 'History',
  culture: 'Culture',
  nature: 'Nature',
  urban: 'Urban',
  personal: 'Personal',
};
