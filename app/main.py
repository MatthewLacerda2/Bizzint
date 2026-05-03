import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from .llms import get_llms_txt
from .core.rate_limiter import limiter
from .core.logging_middleware import LoggingMiddleware
from .core.scheduler import setup_scheduler_jobs, start_scheduler, stop_scheduler
from .api.endpoints import router as api_router
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    setup_scheduler_jobs()
    start_scheduler()

    yield
    stop_scheduler()

app = FastAPI(
    title="BizzInt",
    description="API for the Biss Int.",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(LoggingMiddleware)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root(request: Request):
    return {"message": "Welcome to Biss Int. API"}

@app.get("/health")
async def health(request: Request):
    return {"message": "Welcome to Biss Int. API"}

SECURITY_TXT = "Contact: matheus.l1996@gmail.com\n"
@app.get("/security.txt", response_class=PlainTextResponse)
async def security_txt_fallback():
    return SECURITY_TXT

@app.get("/llms.txt", response_class=PlainTextResponse)
async def llms_txt():
    return get_llms_txt()