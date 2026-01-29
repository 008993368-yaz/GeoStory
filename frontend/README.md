# GeoStory Frontend

A modern, production-ready React + TypeScript application built with Vite.

## Tech Stack

- **React 18** - UI library with functional components and hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **ESLint** - Code linting
- **Prettier** - Code formatting

## Project Structure

```
src/
├── main.tsx              # Application entry point
├── App.tsx               # Root component with routing
├── pages/                # Page components
│   ├── Home.tsx          # Home page with story listing
│   └── StoryCreate.tsx   # Story creation form
├── components/           # Reusable components
│   ├── layout/
│   │   └── AppLayout.tsx # Main layout wrapper
│   └── story/
│       └── StoryCard.tsx # Story card component
├── services/             # API and external services
│   └── api.ts            # Axios instance with interceptors
├── styles/               # Global styles and design tokens
│   ├── tokens.css        # CSS variables (colors, spacing, typography)
│   └── global.css        # Global styles and resets
└── types/                # TypeScript type definitions
    └── index.ts          # Shared types and interfaces
```

## Getting Started

### Prerequisites

- Node.js (v18 or higher recommended)
- npm or yarn

### Installation

1. Install dependencies:

```bash
npm install
```

2. Create environment file:

```bash
cp .env.example .env
```

3. Update `.env` with your API endpoint if needed:

```
VITE_API_URL=http://localhost:8000
```

### Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

### Build

Build for production:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

### Code Quality

Run ESLint:

```bash
npm run lint
```

Format code with Prettier:

```bash
npm run format
```

## Testing

Run tests in watch mode:

```bash
npm run test
```

Run tests once (CI mode):

```bash
npm run test:ci
```

### Testing Stack

- **Vitest** - Fast unit testing framework compatible with Vite
- **@testing-library/react** - React component testing utilities
- **jsdom** - DOM simulation for Node.js
- **@testing-library/jest-dom** - Custom DOM matchers

### Test Structure

```
src/
├── test/
│   ├── setup.ts              # Vitest setup, Calcite stubs, matchMedia mock
│   ├── renderWithRouter.tsx  # MemoryRouter wrapper for route-dependent tests
│   └── __mocks__/            # Module mocks
│       └── arcgis-core/      # Lightweight ArcGIS mocks
├── pages/
│   └── __tests__/
│       ├── Home.test.tsx         # Home page smoke tests
│       └── StoryCreate.test.tsx  # Story creation page tests
└── components/
    └── map/
        └── __mocks__/        # Map component mocks
            ├── MapView.tsx
            └── LocationPickerMap.tsx
```

### Testing Notes

**Calcite Design System:**
Calcite components are custom elements that need stubs in jsdom. The `setup.ts` file defines empty custom elements for all Calcite components used in the app.

**ArcGIS Mocking:**
ArcGIS JS API modules are ~2GB and cause memory issues in tests. We use Vite aliases in `vite.config.ts` to replace them with lightweight mocks that return stub objects:

```typescript
// vite.config.ts test aliases (excerpt)
alias: {
  '@arcgis/core/Map': './src/test/__mocks__/arcgis-core/Map.ts',
  '@arcgis/core/views/MapView': './src/test/__mocks__/arcgis-core/MapView.ts',
  // ... more aliases
}
```

**Memory Management:**
Tests use `pool: 'forks'` (child processes) instead of threads for better memory isolation when ArcGIS modules slip through.

## Features

- ✅ Strict TypeScript configuration
- ✅ React Router for navigation
- ✅ Axios with request/response interceptors
- ✅ CSS custom properties for theming
- ✅ ESLint + Prettier for code quality
- ✅ Environment variable support
- ✅ Production-ready build configuration
- ✅ Clean, scalable folder structure
- ✅ Vitest smoke tests for pages
- ✅ Calcite Design System integration
- ✅ ArcGIS JS API for interactive maps

## API Integration

The application is configured to proxy API requests to `/api` endpoints. Configure the backend URL in `.env`:

```
VITE_API_URL=http://your-backend-url
```

API client is located in `src/services/api.ts` with:
- Automatic auth token injection
- Global error handling
- Request/response interceptors

## Next Steps

- Add photo upload support
- Implement user authentication (OAuth2)
- Add map clustering for many pins
- Improve test coverage for form interactions

## License

MIT
