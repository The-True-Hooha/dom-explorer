from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.core import app_setting
from app.schema.schema import TokenData, UserCreate
from app.database.database import get_database, User

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


async def get_auth_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="oops, jwt invalid",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token=app_setting.JWT_TOKEN,
                             algorithms=[app_setting.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
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
