# iNHCES Backend — Dockerfile
# FastAPI 0.110 + Uvicorn on Python 3.12-slim
# TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
#
# Build:  docker build -t nhces-backend .
# Run:    docker run -p 8000:8000 --env-file .env nhces-backend

# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

# System dependencies required to compile certain Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy only requirements first to leverage Docker layer cache
COPY requirements.txt .

# Install production-only dependencies into a prefix directory
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir --prefix=/install \
        $(grep -v '^\s*pytest\|^\s*httpx\|^\s*pytest-asyncio' requirements.txt | grep -v '^#' | grep -v '^\s*$')

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# libgomp1 is required at runtime by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN groupadd -r nhces && useradd -r -g nhces -d /app -s /sbin/nologin nhces

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ ./app/

# Pre-create directories that the app writes to at runtime
RUN mkdir -p /app/models /app/tmp \
 && chown -R nhces:nhces /app

USER nhces

# Health check — Railway uses this to determine container readiness
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" \
    || exit 1

EXPOSE 8000

# Uvicorn: bind 0.0.0.0 so Railway's load balancer can reach it.
# Workers=1 keeps the LightGBM champion model in a single process (avoids
# per-worker model reload). Increase for CPU-bound workloads once model
# is shared via a sidecar or Redis cache.
CMD ["python", "-m", "uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--log-level", "info", \
     "--access-log"]
