from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./dom_explorer.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    domain_name = relationship("Domain", back_populates="user")
    createdDate = Column(DateTime(timezone=True), server_default=func.now())
    

class Domain(Base):
    __tablename__ = "domain"

    id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String, index=True)
    isActive = Column(Boolean, default=True)
    sub_domain_name = relationship("SubDomain", back_populates="domain_name")
    user = relationship("User", back_populates="domain_name")
    createdDate = Column(DateTime(timezone=True), server_default=func.now())
    
    
class SubDomain(Base):
    __tablename__ = "sub_domain"
    id = Column(Integer, primary_key=True, index=True)
    ctId = Column(String)
    domain_name = relationship("Domain", back_populates="sub_domain_name")
    issueName = Column(String)
    createdDate = Column(DateTime(timezone=True), server_default=func.now())