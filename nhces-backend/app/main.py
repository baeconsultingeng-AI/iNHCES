from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import get_settings

# Routers — imported after they are implemented in S3/S4
# from app.routers import estimate, macro, projects, reports, pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: pre-load the champion ML model into memory.
    Shutdown: nothing required (model lives in process memory).
    """
    settings = get_settings()
    from app.ml.inference import load_champion_model
    load_champion_model()
    print(f"[iNHCES] Starting in {settings.environment} mode")
    yield
    print("[iNHCES] Shutting down")


settings = get_settings()

app = FastAPI(
    title="iNHCES API",
    description=(
        "Intelligent National Housing Cost Estimating System — "
        "REST API for ML-based Nigerian housing construction cost estimation. "
        "TETFund NRF 2025 | ABU Zaria"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS — allow the Next.js frontend and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
from app.routers import estimate
app.include_router(estimate.router, prefix="/estimate", tags=["Estimate"])

from app.routers import macro, projects, reports, pipeline
app.include_router(macro.router,    prefix="/macro",    tags=["Macro"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(reports.router,  prefix="/reports",  tags=["Reports"])
app.include_router(pipeline.router, prefix="/pipeline", tags=["Pipeline"])


# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return JSONResponse({
        "system": "iNHCES API",
        "version": "1.0.0",
        "status": "operational",
        "environment": settings.environment,
        "docs": "/docs",
    })


@app.get("/health", tags=["Health"])
async def health():
    from app.database import health_check
    db_status = health_check()
    overall = "ok" if db_status["status"] == "ok" else "degraded"
    return JSONResponse({
        "status":    overall,
        "db":        db_status,
        "ml_model":  "loaded" if __import__('app.ml.inference', fromlist=['_champion_cache'])._champion_cache else "not_loaded",
    })
