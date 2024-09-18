from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from app.database.database import RoleEnum


class SubDomainBase(BaseModel):
    name: str


class SubDomainCreate(SubDomainBase):
    pass


class SubDomainResponse(SubDomainBase):
    id: int
    createdDate: datetime
    domain_id: int

    class ConfigDict:
        from_attributes = True

class DomainBase(BaseModel):
    domain: str


class DomainCreate(DomainBase):
    isActive: bool = True


class DomainResponse(DomainBase):
    count: int
    regular: List[str] = []
    wildcards: List[str] = []

    class ConfigDict:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: Optional[List[RoleEnum]] = None

class Token(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    token_type: str = Field(..., alias="tokenType")
    exp: datetime

    class ConfigDict:
        populate_by_name = True


class TokenData(BaseModel):
    email: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: str
    domains: List[DomainBase] = []
    createdDate: datetime
    token: Optional[Token] = None

    class ConfigDict:
        from_attributes = True


