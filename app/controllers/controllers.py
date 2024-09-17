from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.schema.schema import UserCreate, UserResponse, DomainResponse
from app.database.database import User, Domain, SubDomain, get_database
from app.service.search_enumerator import get_subdomain_data

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK, description="Get the health status of the database and server")
def run_health_check(db: Session = Depends(get_database)):
    try:
        print("hello world, from db check")
        db.execute(text("SELECT 1"))
        return {
            "server_status": "OK",
            "database": "responsive"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.post('/user', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_database)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.get("/search", response_model=DomainResponse)
async def search_sub_domain(domain:str):
    print('hello world', "from the east", domain)
    data = await get_subdomain_data(domain)
    return data


# @router.get('/users/{user_id}', response_model=UserResponse)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @router.get('/users', response_model=List[UserResponse])
# def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = get_users(db, skip=skip, limit=limit)
#     return users

# Add more routes as needed
