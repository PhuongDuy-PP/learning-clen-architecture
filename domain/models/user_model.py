from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from frameworks.database.database import Base

class UserModel(Base):
    __tablename__ = 'users'

    user_id = Column(String(36), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(64), nullable=False)  # SHA-256 hash is 64 characters
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserModel(username='{self.username}', email='{self.email}')>" 