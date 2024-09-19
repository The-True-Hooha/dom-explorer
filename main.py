import uvicorn
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
