from fastapi import FastAPI
import uvicorn

from app.database.database import Base, engine
from app.core.core import app_setting
from app.controllers.controllers import router as routes

app = FastAPI(title=app_setting.APP_NAME)


app.include_router(routes, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
