# Story List UI Tests

This document contains example tests for the Story List UI feature. The tests are written using Vitest and React Testing Library.

## Setup Required

To run these tests, install the following dependencies:

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom @vitest/ui
```

Then add to `vite.config.ts`:

```typescript
/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test-setup.ts',
  },
});
```

Create `src/test-setup.ts`:

```typescript
import '@testing-library/jest-dom';
```

Add to `package.json`:

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui"
  }
}
```

## Test File: `src/__tests__/Home.test.tsx`

See the example test implementation in the comments below. The tests cover:

- ✅ Loading state rendering
- ✅ Empty state with "Create First Story" CTA
- ✅ Empty state with filter message when filters applied
- ✅ Story rendering in list view
- ✅ Story rendering in timeline view with date headers
- ✅ View toggle (List ↔ Timeline)
- ✅ Pagination controls (Next/Previous buttons)
- ✅ Pagination state (disable buttons appropriately)
- ✅ Category filtering
- ✅ Debounced search input (300ms delay)
- ✅ Error handling and retry functionality
- ✅ URL state management (filters preserved in query params)

## Key Test Patterns

### Mocking the API Service

```typescript
vi.mock('../services/stories');

const mockResponse: StoryListResponse = {
  items: [...],
  total: 10,
  limit: 20,
  offset: 0,
};

vi.mocked(storiesService.listStories).mockResolvedValue(mockResponse);
```

### Testing Debounced Input

```typescript
await user.type(searchInput, 'test');
expect(storiesService.listStories).not.toHaveBeenCalled();

await waitFor(() => {
  expect(storiesService.listStories).toHaveBeenCalledWith(
    expect.objectContaining({ q: 'test' })
  );
}, { timeout: 500 });
```

### Testing Pagination

```typescript
const nextButton = screen.getByRole('button', { name: /next page/i });
await user.click(nextButton);

expect(storiesService.listStories).toHaveBeenCalledWith(
  expect.objectContaining({ offset: 2 })
);
```

### Testing URL State

```typescript
await user.click(timelineButton);

await waitFor(() => {
  expect(window.location.search).toContain('view=timeline');
});
```

## Running Tests

```bash
npm test              # Run tests in watch mode
npm test -- --run     # Run tests once
npm run test:ui       # Open Vitest UI
```

## Coverage

To enable coverage reporting:

```bash
npm test -- --coverage
```
