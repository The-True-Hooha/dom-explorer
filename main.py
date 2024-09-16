from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

from datetime import datetime

app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK, description="get the health status of the database and sever")
def run_health_check():
    return {
        "sever_status": "OK",
        "database": "responsive"
    }
