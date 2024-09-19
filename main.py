from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from app.database.database import Base, engine
from app.core.core import app_setting
from app.controllers.controllers import router as routes

app = FastAPI(title=app_setting.APP_NAME, version="1.0.0",
              description="some OSINT tool")

Base.metadata.create_all(bind=engine)

app.include_router(routes, prefix="/api/v1")


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {str(err)}"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
