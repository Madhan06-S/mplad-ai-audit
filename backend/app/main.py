import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "backend", "app"))

from routers import projects, analytics, reports

app = FastAPI(
    title="SIH26102 — MPLAD AI Governance Intelligence Platform API",
    description="AI-Powered Monitoring, Anomaly Detection & Decision Support Engine for MPLADS.",
    version="2.0.0"
)

# Enable CORS for React Frontend Development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(projects.router)
app.include_router(analytics.router)
app.include_router(reports.router)

# Serve built static frontend dist if available
FRONTEND_DIST = os.path.abspath(os.path.join(BASE_DIR, "frontend", "dist"))
if os.path.exists(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

    @app.get("/")
    def serve_frontend():
        from fastapi.responses import FileResponse
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "status": "online",
            "system": "SIH26102 MPLAD AI Governance Intelligence Platform",
            "version": "2.0.0",
            "docs_url": "/docs"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
