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
