from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    id: int
    createdDate:datetime
    
    class Config:
        orm_mode: True

class DomainBase(BaseModel):
    domain_name: string

class DomainCreate(DomainBase):
    pass

class Domain(DomainBase):
    id: int
    isActive: bool
    createdDate: datetime
    user_id: int
    
    class config:
        orm_mode = True
    
class SubDomainBase(BaseModel):
    ctId: int
    issueName: str
    

class SubDomainCreate(SubDomainBase):
    pass


class SubDomain(SubDomainBase):
    id: int
    createdDate: datetime
    domainId: int
    
    class config:
        orm_mode: True
    

class DomainWithSubDomains(Domain):
    sub_domain: List[SubDomain]
    
    
class UserWithDomain(User):
    domains: List[Domain]


class Token(BaseModel):
    accessToken: str
    tokenType: str
    exp: datetime
    
class TokenData(BaseModel):
    email: Optional[str] = None