import uvicorn
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database.database import Base, engine
from app.core.core import app_setting
from app.controllers.controllers import router as routes

app = FastAPI(title=app_setting.APP_NAME, version="1.0.0",
              description="some OSINT tool")

logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)

app.include_router(routes, prefix="/api/v1")


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
