from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


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
    # id: int
    # isActive: bool
    # createdDate: datetime
    # user_id: int
    count: int
    regular: List[str] = []
    wildcards: List[str] = []

    class ConfigDict:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    domains: List[DomainBase] = []
    createdDate: datetime

    class ConfigDict:
        from_attributes = True


class Token(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    token_type: str = Field(..., alias="tokenType")
    exp: datetime

    class ConfigDict:
        populate_by_name = True


class TokenData(BaseModel):
    email: Optional[str] = None
