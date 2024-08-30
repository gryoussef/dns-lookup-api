import time
import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app, Counter, Histogram
from contextlib import asynccontextmanager
from src.dependencies import get_database, get_utils
from src.api import router
from src.settings import settings


# Initialize FastAPI app
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total number of HTTP requests', 
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'HTTP request latency in seconds', 
    ['method', 'endpoint']
)

# Middleware to collect metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    request_latency = time.time() - start_time
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, request.url.path).observe(request_latency)
    return response


# Mount Prometheus metrics app
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


# Include API router
app.include_router(router, dependencies=[Depends(get_database), Depends(get_utils)])


# Health check endpoint
@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    database = get_database()
    # Startup event
    await database.connect()
    await database.create_tables()
    yield
    # Shutdown event
    await database.disconnect()


app.router.lifespan_context = lifespan


if __name__ == "__main__":

    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=3000,
        log_level="info",
        access_log=True
    )
