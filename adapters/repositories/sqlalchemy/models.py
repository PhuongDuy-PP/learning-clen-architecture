from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base, validates
import uuid
import re

# Base class for declarative models
Base = declarative_base()


class UserModel(Base):
    """
    SQLAlchemy model for users with code-first approach
    Includes validation and default values
    """

    __tablename__ = "users"

    # Use String as primary key with UUID string
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Username with length constraints
    username = Column(String(50), nullable=False, unique=True)

    # Email with validation
    email = Column(String(255), nullable=False, unique=True)

    # Password hash with fixed length for SHA-256
    password_hash = Column(String(64), nullable=False)

    # Active status with default
    is_active = Column(Boolean, default=False)

    # Timestamps with automatic management
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    @validates("email")
    def validate_email(self, key, email):
        """
        Email validation during model creation
        """
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise ValueError(f"Invalid email address: {email}")
        return email

    @validates("username")
    def validate_username(self, key, username):
        """
        Username validation during model creation
        """
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return username


class RoleModel(Base):
    """
    Example of an additional model to demonstrate relationships
    """

    __tablename__ = "roles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))

    # Can add more role-related fields as needed
