from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    email = Column(String(255), index=True, nullable=False)
    username = Column(String, primary_key=True, nullable=False)
    app_name = Column(String(255), primary_key=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    role = Column(String(50), nullable=False, default="user", index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
