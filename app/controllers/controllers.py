from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.schema.schema import UserCreate, DomainResponse, Token, CreateUserResponse, LoginData, LoginResponse
from app.database.database import User, Domain, SubDomain, get_database
from app.service.search_enumerator import get_subdomain_data
from app.service.service import create_new_user, create_access_token, get_auth_user, isAdmin, get_user, login_user, get_my_profile

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK, description="Get the health status of the database and server")
def run_health_check(db: Session = Depends(get_database)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "server_status": "OK",
            "database": "responsive"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.get("/search", response_model=DomainResponse)
async def search_sub_domain(domain: str):
    print('hello world', "from the east", domain)
    data = await get_subdomain_data(domain)
    return data


@router.post("/user", response_model=CreateUserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_database)):
    new_user = create_new_user(user=user, db=db)
    return new_user


@router.post("/login", response_model=LoginResponse)
def handle_login_user(data: LoginData, db: Session = Depends(get_database)):
    return login_user(db, email=data.email, password=data.password)

@router.get("/profile/me")
def my_profile(user: User = Depends(get_auth_user), db: Session = Depends(get_database)):
    print("does anything happen here", db)
    return get_my_profile(user, db)
