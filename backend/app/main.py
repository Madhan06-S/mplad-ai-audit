from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import projects, analytics, reports

app = FastAPI(
    title="SIH26102 — MPLAD AI Audit Platform API",
    description="AI-Powered Monitoring, Anomaly Detection & Risk Engine REST Services for MPLADS",
    version="1.0.0"
)

# CORS Middleware (Enable for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(projects.router)
app.include_router(analytics.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "SIH26102 MPLAD AI Audit API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
