from sqlalchemy import create_engine, Time, Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from app.core.core import app_setting
import datetime
import enum
import pytz

SQLALCHEMY_DATABASE_URL = app_setting.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False},
                       )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class RoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"
    support = "support"
    other = "other"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)
    domains = relationship("Domain", back_populates="user")
    createdDate = Column(DateTime, server_default=func.now())
    
    def __str__(self):
        return f"User(id={self.id}, email='{self.email}', role='{self.role}', createdDate='{self.createdDate}', domains='{self.domains[:5]}'),"
    
    def __repr__(self):
        return self.__str__()

class Domain(Base):
    __tablename__ = "domain"

    id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String, index=True)
    isActive = Column(Boolean, default=True)
    sub_domains = relationship("SubDomain", back_populates="domain")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="domains")
    createdDate = Column(DateTime(timezone=True),
                         default=datetime.datetime.utcnow)
    
    def __str__(self):
        return f"Domain(id={self.id}, name='{self.domain_name}', active={self.isActive}, user_id={self.user_id}, createdDate={self.createdDate})"

    def __repr__(self):
        return self.__str__()


class SubDomain(Base):
    __tablename__ = "sub_domain"

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey('domain.id'))
    domain = relationship("Domain", back_populates="sub_domains")
    name = Column(String)
    createdDate = Column(DateTime(timezone=True),
                         default=datetime.datetime.utcnow)
    
    def __str__(self):
        return f"SubDomain(id={self.id}, name='{self.name}', domain_id={self.domain_id})"

    def __repr__(self):
        return self.__str__()


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
