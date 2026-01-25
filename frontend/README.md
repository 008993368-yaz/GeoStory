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

## Features

- ✅ Strict TypeScript configuration
- ✅ React Router for navigation
- ✅ Axios with request/response interceptors
- ✅ CSS custom properties for theming
- ✅ ESLint + Prettier for code quality
- ✅ Environment variable support
- ✅ Production-ready build configuration
- ✅ Clean, scalable folder structure

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

- Add Calcite Design System components
- Integrate ArcGIS JS API for mapping features
- Implement authentication
- Add state management (if needed)
- Set up testing framework

## License

MIT
