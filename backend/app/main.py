"""
SuperQuantLab 2.0 Backend - FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import backtest_router, strategies_router, metrics_router

# Create FastAPI app
app = FastAPI(
    title="SuperQuantLab 2.0 API",
    description="Crypto Quant Trading Engine API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(backtest_router, prefix=settings.api_v1_prefix)
app.include_router(strategies_router, prefix=settings.api_v1_prefix)
app.include_router(metrics_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "SuperQuantLab 2.0",
        "version": "2.0.0",
        "description": "Crypto Quant Trading Engine",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

