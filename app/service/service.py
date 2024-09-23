import bcrypt
import logging

from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload
from fastapi.responses import RedirectResponse


from app.core.core import app_setting
from app.schema.schema import TokenData, UserCreate, UserBase, ApiResponseModel, ProfileResponse
from app.database.database import get_database, User, Domain, SubDomain


logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(password: str, hashed_password: str):
    pwd_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password=pwd_bytes, hashed_password=hashed_password)


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)


def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def login_user(db: Session, email: str, password: str):
    user: User = get_user(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="email or password incorrect"
        )
    token = create_access_token(data={"email": email})
    logger.info(f"new user login from {email}")
    return {
        "message": "successfully logged in",
        "token": token
    }
    

def create_access_token(data: dict, expiry: Optional[timedelta] = None):
    to_encode = data.copy()
    if expiry:
        expire = datetime.utcnow() + expiry
    else:
        expire = datetime.utcnow() + timedelta(minutes=6*60)  # set the expiry to 6 hours
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, app_setting.JWT_TOKEN,
                       algorithm=app_setting.ALGORITHM)
    return {
        "token": token,
        "expiresAt": expire
    }

async def get_user_from_cookie(req:Request, db:Session = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="oops, seems you are not authorized",
        headers={"WWW-Authenticate": "Bearer"}
    )
    access_token = req.cookies.get("dom_explorer")
    if not access_token:
        print(access_token)
        RedirectResponse(url="/login")
    else:
        # raise credentials_exception
        token = access_token.split()[1]
        return await get_auth_user(db=db, token=token)

async def get_auth_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="oops, seems you are not authorized",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token,
            app_setting.JWT_TOKEN,
            algorithms=[app_setting.ALGORITHM]
        )
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = UserBase(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def create_new_user(db: Session, user: UserCreate):
    find_user = get_user(db, email=user.email)
    if find_user:
        raise HTTPException(
            status_code=400, detail="oops, email already registered")
    hashed_password = get_password_hash(user.password)
    created_user = User(
        email=user.email, password=hashed_password, role=user.role)
    token = create_access_token(data={"email": created_user.email})
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    logger.info(f"new account created by {created_user.email}")
    return {
        "message": "successfully created account",
        "user": created_user,
        "token": token
    }


def isAdmin(user: User = Depends(get_auth_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Not Authorized"
        )
    return user


def get_user_relation(db: Session, email: str):
    return db.query(User).options(
        joinedload(User.domains).joinedload(Domain.sub_domains)
    ).filter(User.email == email).first()


def get_my_profile(user: User, db: Session):
    logger.info(f"getting user profile {user.email}")
    data: User = get_user_relation(db, email=user.email)
    map_profile = map_user_with_domain_response(data)
    return ApiResponseModel(
        message="successful",
        status_code=status.HTTP_200_OK,
        data=map_profile
    )


def map_user_with_domain_response(user: User) -> ProfileResponse:
    return ProfileResponse(
        id=str(user.id),
        email=user.email,
        role=user.role,
        created_date=user.createdDate,
        domains=[
            ProfileDomain(
                id=domain.id,
                domain=domain.domain_name,
                isActive=domain.isActive,
                createdDate=domain.createdDate,
                sub_domain=[
                    SubDomainResponse(
                        regular=sub_domain.regular,
                        wildcards=sub_domain.wildcards,
                    ) for sub_domain in domain.sub_domains
                ]
            ) for domain in user.domains
        ]
    )
    

def get_domain_by_id(user: User, db: Session) -> Domain:
    return db.query(Domain).filter(Domain.user_id == user_id).all()


def get_user_domains(db: Session, user: User, skip: int = 0, limit: int = 10) -> Tuple[List[Domain], int]:
    query = db.query(Domain).filter(Domain.user_id == user.id)
    total = query.count()
    domains = query.offset(skip).limit(limit).all()
    return domains, total


def get_user_domain_with_subdomains(db: Session, user: User, id: int, skip: int = 0, limit: int = 10) -> Tuple[Domain, int]:
    domain:Domain = db.query(Domain).filter(
        Domain.id == id,
        Domain.user_id == user.id
    ).first()

    if domain:
        subdomains_query = db.query(SubDomain).filter(
            SubDomain.domain_id == domain.id)
        total_subdomains = subdomains_query.count()
        subdomains = subdomains_query.offset(skip).limit(limit).all()
        domain.sub_domains = subdomains
        return domain, total_subdomains
    return None, 0