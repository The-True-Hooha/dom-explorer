from fastapi import APIRouter, HTTPException, Depends, status, Request, Query, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.core.core import limiter

from app.schema.schema import UserCreate, DomainResponse, Token, CreateUserResponse, LoginData, LoginResponse, PaginatedDomainsResponse, PaginatedSubDomainsResponse, SubdomainSearchResponse
from app.database.database import User, Domain, SubDomain, get_database
from app.service.search_enumerator import get_subdomain_data, get_updated_domains
from app.service.service import create_new_user, create_access_token, get_user_from_cookie, isAdmin, get_user, login_user, get_my_profile, get_user_domain_with_subdomains, get_user_domains, get_auth_user

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
@limiter.limit("5/minute")
async def search_sub_domain(domain: str, request: Request, user: User = Depends(get_user_from_cookie), db: Session = Depends(get_database)):
    data = await get_subdomain_data(domain, db, user)
    return data


@router.post("/signup", response_model=CreateUserResponse)
@limiter.limit("5/minute")
def create_user(user: UserCreate, response: Response, request: Request, db: Session = Depends(get_database)):
    new_user = create_new_user(user=user, db=db)
    response.set_cookie(
        key="dom_explorer",
        value=f"Bearer {new_user["token"]["token"]}",
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=14 * 24 * 60 * 60
    )
    return new_user


@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
def handle_login_user(data: LoginData, request: Request, response: Response, db: Session = Depends(get_database)):
    data = login_user(db, email=data.email, password=data.password)
    response.set_cookie(
        key="dom_explorer",
        value=f"Bearer {data["token"]["token"]}",
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=14 * 24 * 60 * 60,
    )
    return data


@router.get("/profile/me")
@limiter.limit("5/minute")
def my_profile(request: Request, user: User = Depends(get_user_from_cookie), db: Session = Depends(get_database)):
    return get_my_profile(user, db)


@router.get("/domains", response_model=PaginatedDomainsResponse)
@limiter.limit("10/minute")
async def get_user_domains(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_user_from_cookie),
    db: Session = Depends(get_database)
):
    domains, total = get_user_domains(db, current_user, skip, limit)
    return PaginatedDomainsResponse(
        domains=domains,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/domains/{id}")
@limiter.limit("10/minute")
async def read_user_domain(
    request: Request,
    id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_user_from_cookie),
    db: Session = Depends(get_database)
):
    domain, total_subdomains = get_user_domain_with_subdomains(
        db, current_user, id, skip, limit)
    if domain is None:
        raise HTTPException(status_code=404, detail="Domain cannot be found")
    return {
        "domain": domain,
        "sub_domains": domain.sub_domains,
        "total_subdomains": total_subdomains,
        "skip": skip,
        "limit": limit
    }


@router.get("/domain/check-updates")
@limiter.limit("5/minute")
async def get_domain_updates(request: Request, domain: str, user: User = Depends(get_user_from_cookie), db: Session = Depends(get_database)):
    data = await get_updated_domains(db=db, domain=domain, user=user)
    return SubdomainSearchResponse(**data)
