# GeoStory Interview Notes

Quick reference for demonstrating and discussing the GeoStory project in interviews.

---

## 60-Second Pitch

> "GeoStory is a location-based storytelling platform where users can share stories tied to geographic locations. I built the full stack: a **React + TypeScript** frontend using Esri's **Calcite Design System** and **ArcGIS JS API** for mapping, backed by a **FastAPI** REST API with **async SQLAlchemy** and **PostgreSQL**.
>
> The core feature is an interactive map where users can browse stories as pins, filter by category or date, and create new stories by clicking a location. The architecture uses modern async patterns throughout, with URL-based state management for shareable filtered views and comprehensive test coverage using pytest (100 tests) and Vitest.
>
> This demonstrates my ability to build complete applications with production-quality code, proper testing, and clean architecture."

---

## 3-Minute Demo Script

### Part 1: Browse Stories (1 min)
1. Open Home page → show map with story pins
2. Click a pin → story card highlights, map pans
3. Click different card → pin highlights
4. Apply filters: select category, search text
5. Note URL changes with filters (shareable links)

### Part 2: Create Story (1 min)
1. Click "Create Story" button
2. Fill in title, body, category
3. Click on map to set location
4. Select story date
5. Submit → see success feedback
6. New story appears on home map

### Part 3: Under the Hood (1 min)
1. Show FastAPI auto-docs at `/docs`
2. Demonstrate API call with curl:
   ```bash
   curl http://localhost:8001/api/stories | jq
   ```
3. Mention: "100 backend tests, smoke tests for frontend"
4. Point out: Docker Compose setup for easy onboarding

---

## 5 Technical Talking Points

### 1. REST API Design with FastAPI
> "I chose FastAPI for its excellent async support and automatic OpenAPI documentation. Each endpoint uses Pydantic models for request validation—for example, the `StoryCreate` schema enforces that latitude must be between -90 and 90, categories must be from an enum, and dates can't be in the future. This gives us type safety across the API boundary."

**Follow-up Q:** "How do you handle validation errors?"  
**A:** "Pydantic raises `ValidationError` which FastAPI converts to 422 responses with detailed error messages. I also have custom validators for business rules like the category enum check."

### 2. Async SQLAlchemy with PostgreSQL
> "The backend uses async SQLAlchemy 2.0 with the asyncpg driver. This means database calls are non-blocking—when one request waits for the database, the event loop can handle other requests. The session management uses FastAPI's dependency injection with `async with` for proper transaction handling."

**Follow-up Q:** "What about connection pooling?"  
**A:** "SQLAlchemy's `create_async_engine` manages a connection pool automatically. We configure `pool_size` and `max_overflow` based on expected load."

### 3. Calcite Design System + ArcGIS JS API
> "The frontend uses Esri's Calcite Design System, which provides accessible, consistent UI components that work well with ArcGIS maps. The map component uses the ArcGIS JS API for rendering story pins as graphics, with click handlers for selection. There's bidirectional sync—clicking a pin selects the card, and clicking a card pans the map."

**Follow-up Q:** "How did you handle testing with ArcGIS?"  
**A:** "ArcGIS modules are 2GB+ so I created lightweight mocks using Vite aliases. The mocks return stub objects with the minimum properties our code needs, keeping tests fast."

### 4. URL-Based State Management
> "Filter state lives in URL query params rather than component state. When you filter by category or search, the URL updates. This means filtered views are shareable—you can send someone a link to 'all historical stories about parks'—and browser back/forward works correctly."

**Follow-up Q:** "How do you sync URL with component state?"  
**A:** "React Router's `useSearchParams` hook provides the params. On mount and param change, we parse them into filter state. When user changes a filter, we update the URL, which triggers a re-render."

### 5. Testing Strategy
> "I follow the testing pyramid: many unit tests for business logic, integration tests for API endpoints, and smoke tests for UI. Backend has 100 pytest tests covering CRUD, validation, and edge cases. Frontend has Vitest tests that mock the API and verify pages render correctly."

**Follow-up Q:** "How do you test async database code?"  
**A:** "Each test gets an isolated async session. Tests create their own data, run assertions, and the session is rolled back—no test pollution."

---

## 3 Architecture Tradeoffs

### 1. Monolith vs. Microservices
> **Decision:** Single FastAPI backend (monolith)
> 
> **Why:** For an MVP, microservices add operational complexity without benefit. A single service is easier to develop, test, and deploy. The code is organized in modules (routers, crud, schemas) so it could be split later if needed.
> 
> **Tradeoff:** Scales vertically for now; horizontal scaling would require careful session/connection management.

### 2. Client-Side vs. Server-Side Rendering
> **Decision:** Client-side SPA with Vite + React
> 
> **Why:** The app is highly interactive (map interactions, filtering, forms). SSR's SEO benefits don't apply to a logged-in app. Vite provides fast HMR for development.
> 
> **Tradeoff:** Initial load is heavier; could add code splitting for production.

### 3. Sync vs. Async Database Access
> **Decision:** Fully async with asyncpg
> 
> **Why:** FastAPI is async-native, and async DB access avoids blocking the event loop. Better concurrency under load.
> 
> **Tradeoff:** Async code is more complex; must be careful with session lifecycle and avoid mixing sync operations.

---

## Common Interview Questions

### "What would you do differently?"
- Add error boundaries in React for graceful failure
- Implement proper logging (structured JSON logs)
- Add integration tests that hit real API + DB together
- Set up CI/CD with GitHub Actions from day one

### "How would you scale this?"
- Add read replicas for query-heavy workloads
- Implement caching (Redis) for hot story lists
- Use PostGIS for spatial indexing as stories grow
- Add CDN for static assets and photo storage

### "What's the hardest bug you fixed?"
- "ArcGIS modules are ~2GB and caused JavaScript heap out of memory errors in tests. I solved it by creating lightweight mocks using Vite's alias configuration, so tests load fake modules instead of the real ArcGIS SDK."

### "Why not [alternative technology]?"
- **Why not Django?** FastAPI is more modern, async-native, and has better typing support
- **Why not MongoDB?** Relational data (stories, users, photos) with foreign keys fits SQL better
- **Why not Redux?** URL state + React's useState is simpler for this app's complexity level

---

## Quick Facts

| Metric | Value |
|--------|-------|
| Backend tests | 100 passing |
| Frontend tests | 9 smoke tests |
| API endpoints | 3 (create, list, get) |
| Database tables | 3 (stories, users, photos) |
| Lines of Python | ~2,000 |
| Lines of TypeScript | ~1,500 |
| Setup time | <5 min with Docker |

---

## Links to Show

1. **Live Demo:** `http://localhost:5173` (frontend)
2. **API Docs:** `http://localhost:8001/docs` (Swagger UI)
3. **Architecture Doc:** `docs/ARCHITECTURE.md`
4. **Database Schema:** `docs/schema.md`
