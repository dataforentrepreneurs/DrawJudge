---
description: DrawJudge Project Overview and Architecture
---

# DrawJudge 🎨⚖️ - Project Overview

## 1. Introduction
DrawJudge is a real-time, multiplayer browser party game where users are given a prompt, draw their interpretation on a shared canvas, and submit it to an AI Judge. The AI evaluates the drawings based on creativity, clarity, entertainment, and prompt relevance.

## 2. Technology Stack
### Frontend
- **Framework**: React 19 (Single Page Application)
- **Build Tool**: Vite
- **Language**: TypeScript (`.tsx`)
- **Styling**: Tailwind CSS / Custom CSS (`index.css`)
- **Key Modules**: Lucide-React (Icons), QRCode.react (Lobby joining)

### Backend
- **Framework**: FastAPI (Python)
- **Server**: Uvicorn (ASGI)
- **Real-Time Communication**: WebSockets (`websockets` library)
- **Data Validation**: Pydantic
- **AI Integration**: Google Generative AI (`google-genai` SDK) using `gemini-2.5-flash`
- **Type Checking**: Pyre (Meta's static type checker)

### DevOps & Deployment
- **Containerization**: Docker (`Dockerfile`)
- **Hosting / PaaS**: Render (`render.yaml` spec for auto-deployment)
- **CI/CD**: GitHub Actions (`.github/workflows/ci.yml`)

---

## 3. Architecture & Core Workflows

### 3.1 Server Architecture
The backend is fundamentally structured to handle both REST API calls (for room creation) and persistent WebSocket connections (for game loop updates). 
- In development, the servers run disjointly (`npm run dev` on 5173, `fastapi dev` on 8000). 
- In production, FastAPI's `StaticFiles` middleware is used to serve the compiled Vite React bundle (`frontend/dist`) directly from the Python server on `/`, while API and WS routes are handled dynamically natively.

### 3.2 State Management (`state_manager.py`)
Currently, game state is stored **IN-MEMORY** using a global Python dictionary `active_rooms`.
- Core entity `RoomState` tracks: `room_code`, `host_id`, `status` (waiting, drawing, judging, results), `players` list, `round_prompt`, `game_mode`, and the base64 encoded image `submissions`.
- Because state is in-memory, the backend is strictly **stateful**. This means it currently cannot be easily horizontally scaled across multiple instances without sticky sessions or a centralized state store.

### 3.3 The Core Game Loop (WebSocket Driven)
1. **Lobby Creation**: Host creates a room (`POST /api/rooms`), receives a room code.
2. **Joining**: Players enter name and code, connecting to `ws://.../ws/rooms/{code}?player_id={id}`. 
3. **Broadcasting**: `websocket_manager.py` maintains the connection pool. Every time a player joins/leaves, it broadcasts a `room_state_update` to all clients in the room.
4. **Drawing Phase**: Host triggers `start_round`. The backend assigns a prompt and broadcasts `round_started`. The React `App.tsx` switches the view to `drawing`.
5. **Submission**: Players submit canvas data (`image_data: data:image/png;base64,...`) via WebSocket event `submit_drawing`.
6. **Judging Phase**: Once all submissions are received (or time expires), the backend shifts state to `judging_started` and triggers `evaluate_submissions()`.

### 3.4 The AI Judge (`ai_judge.py`)
Submissions are evaluated concurrently using `asyncio.gather`.
- **Primary Judge**: Google's `gemini-2.5-flash`. The API takes the system prompt containing instructions alongside the base64-decoded image payload.
- **Scoring Metrics**: `prompt_relevance`, `creativity`, `clarity`, `entertainment`. 
- **Rule Enforcement**: Off-topic drawings (relevance <= 3) receive a massive penalty multiplier in Python to ensure fairness.
- **Mock Fallback**: If the `GEMINI_API_KEY` is completely missing, or if the API request throws an error (e.g., quota exceeded / model name deprecated), the code catches the exception and falls back to a locally generated mock score with `is_mock = True`.

---

## 4. Current Status (As of March 2026)
- **✅ Functional**: The core game loop is fully operational. Players can join, draw, submit, and receive AI scores.
- **✅ Bug Fixes**: The `NOT_FOUND` error regarding Google's legacy 1.5 flash model has been patched. The API correctly utilizes `gemini-2.5-flash`. Pyre module warnings have been corrected with relative search paths.
- **✅ Hosting Configured**: The repository has CI pipelines and Render configuration ready to deploy.

---

## 5. Next Steps & Roadmap

To evolve DrawJudge into a production-ready application, the following steps are recommended:

### Phase 1: Robustness & Scale (Backend)
1. **Migrate State to Redis**: Abstract `state_manager.py` from an in-memory dictionary to Redis. This is critical if the app is ever deployed using multiple Uvicorn workers or serverless containers.
2. **Handle Disconnections Gracefully**: Introduce reconnection windows mechanism. If a player drops WebSocket connection on mobile, they should be able to rejoin seamlessly using their `playerId` cached in `localStorage` without losing their score or round state.
3. **Prompt Library System**: Move hardcoded prompts into an expandable PostgreSQL database or external JSON dictionaries.

### Phase 2: Game Mechanics & Monetization (Frontend)
1. **"DLC" Prompt Packs**: The UI currently has mockup buttons for "NSFW Pack" and "Office Jobs". These need to be activated. 
2. **Host Controls**: Give hosts the ability to manually kick trolls, bypass timers, or choose specific categories.
3. **Enhanced Drawing Tools**: The current canvas is functional but basic. Add flood fill options, varied brush textures, an eraser, and an undo/redo stack in `DrawCanvas.tsx`.

### Phase 3: Analytics & Rate Limiting
1. **API Quota Management**: The Gemini API calls are the biggest failure point (and cost). We need to implement strict rate-limiting per IP/Room to prevent abuse from depleting the API quotas.
2. **Caching Results**: If two identical prompts/images are processed (unlikely but possible), cache the Gemini response to save bandwidth and API limits.
