from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from enum import Enum

class Role:
    ADMIN = 1
    USER = 2

class Roles(str,Enum):
    ADMIN = 'Admin'
    USER = 'User'

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    profilepic = Column(String(255))
    name = Column(String(100))
    cellnumber = Column(String(15), unique=True)
    password = Column(String(255))
    email = Column(String(100), unique=True)
    deletedAt = Column(DateTime, nullable=True)
    created = Column(DateTime, default=datetime.now())
    modified = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    roleId = Column(Integer)

class AccessToken(Base):
    __tablename__ = "accesstoken"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True)
    ttl = Column(Integer)  # in ms
    userId = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    created = Column(DateTime, default=datetime.now())
