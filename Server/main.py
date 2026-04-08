import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import rooms, game
import google.generativeai as genai
import os

print("\n--- SERVER STARTING: VERSION 3 (With Request Logging) ---\n")

app = FastAPI(title="Party Games Hub API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"DEBUG: {request.method} {request.url}")
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# === Unified Gemini Proxy ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_model(model_name="gemini-1.5-flash"):
    return genai.GenerativeModel(model_name)

# Mount modular API routers
app.include_router(rooms.router, prefix="/api/drawjudge")
app.include_router(game.router)

@app.get("/api/health")
async def health_check():
    print("DEBUG: Health check hit")
    return {"status": "ok", "message": "Backend is reachable!"}

# Mount the compiled React Single Page Apps for production serving
launcher_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Games", "Launcher", "dist"))
drawjudge_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Games", "DrawJudge", "dist"))

# Mount assets specifically
if os.path.exists(launcher_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(launcher_dist, "assets")), name="launcher_assets")
if os.path.exists(drawjudge_dist):
    app.mount("/drawjudge/assets", StaticFiles(directory=os.path.join(drawjudge_dist, "assets")), name="drawjudge_assets")

@app.get("/{full_path:path}")
async def serve_frontend(request: Request, full_path: str):
    # CRITICAL: If this is an API or WS request, DO NOT return HTML
    if full_path.startswith("api/") or full_path.startswith("ws/") or "api/" in request.url.path:
        raise HTTPException(status_code=404, detail=f"API route '{full_path}' not found on server.")

    # Handle DrawJudge frontend
    if full_path.startswith("drawjudge"):
        if not os.path.exists(drawjudge_dist):
            return {"error": "DrawJudge frontend not built"}
        dj_path = full_path.replace("drawjudge/", "").replace("drawjudge", "")
        target_path = os.path.join(drawjudge_dist, dj_path)
        if dj_path and os.path.isfile(target_path):
            return FileResponse(target_path)
        return FileResponse(os.path.join(drawjudge_dist, "index.html"))

    # Handle Launcher frontend
    if os.path.exists(launcher_dist):
        target_path = os.path.join(launcher_dist, full_path)
        if os.path.isfile(target_path):
            return FileResponse(target_path)
        return FileResponse(os.path.join(launcher_dist, "index.html"))

    return {"status": "ok", "message": "PartyGamesHub API is running. (React dist folders not found)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
