import uvicorn
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from datetime import datetime

from app.database.database import Base, engine
from app.core.core import app_setting, limiter
from app.controllers.controllers import router as routes

app = FastAPI(title=app_setting.APP_NAME, version="1.0.0",
              description="some OSINT tool")

logger = logging.getLogger(__name__)

app.include_router(routes, prefix="/api/v1")

Base.metadata.create_all(bind=engine)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context = {"current_year": datetime.now().year})

@app.get("/profile")
async def user_profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    errors = exception.errors()
    error_messages = [f"{e['loc'][-1]}: {e['msg']}" for e in errors]
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages, "body": exception.body},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exception: StarletteHTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": exception.detail},
    )
    

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exception: Exception):
    logger.error(f"Unhandled exception: {str(exception)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred. Please try again later.",
            "path": request.url.path
        },
    )
    
# remove when not in production
@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response = await call_next(request)
    if isinstance(response, HTMLResponse):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


        
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
