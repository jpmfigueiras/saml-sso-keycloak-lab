from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes.routes import auth_router

app = FastAPI(
    title=settings.app_name,
    description="API developed with FastAPI",
    version=settings.app_version,
    debug=settings.debug
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "status": "online",
        "version": settings.app_version,
        "environment": settings.environment
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.environment
    }

# To run: uvicorn main:app --reload --host 0.0.0.0 --port 8000
