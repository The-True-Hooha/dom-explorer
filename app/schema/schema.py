from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Union, Optional, Any
from datetime import datetime
from app.database.database import RoleEnum


class SubDomainBase(BaseModel):
    name: str


class SubDomainCreate(SubDomainBase):
    pass


class SubDomainResponse(BaseModel):
    regular: List[str] = []
    wildcards: List[str] = []

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
    role: Optional[str] = None

class Token(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    token_type: str = Field(..., alias="tokenType")
    exp: datetime

    class ConfigDict:
        populate_by_name = True


class TokenData(BaseModel):
    token: str
    expiresAt: datetime


class UserObj(UserBase):
    id: int
    createdDate: datetime
    password: str
    role: Optional[str] = None
class CreateUserResponse(BaseModel):
    message: str
    user: UserObj
    token: TokenData

class LoginData(UserBase):
    password: str
    
class LoginResponse(BaseModel):
    message: str
    token: TokenData
    
class ProfileDomain(BaseModel):
    id: int
    domain: str
    isActive: bool
    createdDate: datetime
    sub_domain: List[SubDomainResponse] = []
    
class ApiResponseModel(BaseModel):
    message: str
    status_code: int
    data: Optional[Union[Any, List[Any]]] = None
    
class ProfileResponse(BaseModel):
    id: str
    email: EmailStr
    created_date: datetime
    role: str
    domains: List[ProfileDomain] = []

    class ConfigDict:
        from_attributes = True
        
