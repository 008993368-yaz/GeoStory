# GeoStory Demo Script

Step-by-step walkthrough for demonstrating GeoStory to interviewers or stakeholders.

---

## Prerequisites

Make sure the stack is running:

```bash
docker compose -f docker-compose.dev.yml up -d
```

Verify services:
- Frontend: http://localhost:5173 ✓
- Backend API: http://localhost:8001/docs ✓
- Database: PostgreSQL on port 5432 ✓

---

## Demo Part 1: Explore Stories (2 min)

### Step 1.1: Open Home Page
1. Navigate to **http://localhost:5173**
2. Wait for map to load (ArcGIS basemap)
3. **Point out:** "This is the main view—an interactive map with story pins"

### Step 1.2: Interact with Map
1. **Click on a pin** on the map
2. **Observe:** Story card highlights in the list below
3. **Say:** "Clicking a pin selects the story. Map and list are synced."

### Step 1.3: Select from List
1. **Click on a different story card** in the list
2. **Observe:** Map pans to that story's location, pin highlights
3. **Say:** "Bidirectional—clicking a card focuses the map too."

### Step 1.4: Filter Stories
1. **Click the Category dropdown** → Select "Historical"
2. **Observe:** Only historical stories show
3. **Point to URL bar:** "Notice the URL now has `?category=historical`"
4. **Type in the Search box:** "park"
5. **Observe:** Results filter further
6. **Say:** "URL-based state means these filtered views are shareable"

### Step 1.5: Clear Filters
1. Click "Clear Filters" button (if available) or remove URL params
2. All stories return

---

## Demo Part 2: Create a Story (2 min)

### Step 2.1: Navigate to Create Form
1. **Click "Create Story" button** in the header/navigation
2. **Observe:** Form page loads with map on the right

### Step 2.2: Fill Out Form
1. **Title:** "My Interview Demo Story"
2. **Body:** "This story was created during a live demo to show the full stack in action."
3. **Category:** Select "Personal"
4. **Say:** "Form uses Calcite Design System components for consistent Esri styling"

### Step 2.3: Pick Location
1. **Click on the map** where you want the story located
2. **Observe:** A marker appears at clicked location
3. **Say:** "Location is required—click-to-select makes it intuitive"

### Step 2.4: Set Date
1. **Click the date picker** → Select today's date
2. **Say:** "Dates are optional, validated to not be in the future"

### Step 2.5: Submit
1. **Click "Submit" or "Create Story" button**
2. **Wait for response** (should be quick, <500ms)
3. **Observe:** Success message appears
4. **Navigate back to Home** (or auto-redirected)
5. **Find your new story** on the map!

---

## Demo Part 3: API Under the Hood (2 min)

### Step 3.1: Show Swagger UI
1. Open new tab: **http://localhost:8001/docs**
2. **Say:** "FastAPI auto-generates these docs from type annotations"
3. **Expand:** `POST /api/stories` endpoint
4. **Point out:** Request schema, response schema, example values

### Step 3.2: Try API Directly
1. In Swagger UI, expand `GET /api/stories`
2. Click **"Try it out"**
3. Leave parameters empty, click **Execute**
4. **Show the response:** JSON with stories array
5. **Say:** "This is the same endpoint the frontend calls"

### Step 3.3: Show Filtering in API
1. In Swagger UI, `GET /api/stories` with **category=historical**
2. Execute and show filtered results
3. **Say:** "Filters are query params—RESTful design"

### Step 3.4: Mention Testing
1. **Say:** "The backend has 100 pytest tests covering all endpoints and edge cases"
2. **Say:** "Frontend has Vitest smoke tests for page rendering"
3. *Optional:* Show terminal with `docker compose exec backend pytest -q`

---

## Demo Part 4: Quick Code Walkthrough (2 min)

### Backend Structure
```
backend/
├── app/
│   ├── main.py         # FastAPI app setup
│   ├── routers/        # API endpoint handlers
│   ├── crud/           # Database operations
│   ├── schemas/        # Pydantic validation
│   └── db/             # SQLAlchemy models
├── alembic/            # Database migrations
└── tests/              # 100 pytest tests
```

**Point out:** "Clean separation of concerns—routers handle HTTP, crud handles DB, schemas handle validation"

### Frontend Structure
```
frontend/
├── src/
│   ├── pages/          # Home, StoryCreate
│   ├── components/     # Map, StoryCard, Layout
│   ├── services/       # API client
│   └── types/          # TypeScript interfaces
└── vite.config.ts      # Build + test config
```

**Point out:** "Standard React structure with TypeScript for type safety"

---

## Talking Points During Demo

| When | Say |
|------|-----|
| Map loads | "ArcGIS JS API with Calcite styling" |
| Filter works | "URL state makes it shareable" |
| Form submits | "Pydantic validates on the backend" |
| API responds | "Async SQLAlchemy—non-blocking" |
| Tests mentioned | "100 backend + 9 frontend tests" |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Map not loading | Check browser console for ArcGIS errors; may need API key |
| API returns 500 | Check `docker compose logs backend` |
| Database empty | Run migrations: `docker compose exec backend alembic upgrade head` |
| Frontend not loading | Check `docker compose logs frontend` |

---

## After Demo: Invite Questions

Good prompts to offer:
- "Any questions about the architecture decisions?"
- "Want to see how the async database code works?"
- "Interested in how I handled testing the map components?"
- "Questions about how this would scale in production?"
