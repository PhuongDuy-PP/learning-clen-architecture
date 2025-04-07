from dataclasses import dataclass
from domain.value_objects.email import Email
from typing import Optional
import hashlib
import uuid

@dataclass
class User:
    username: str
    email: Email
    password_has: str
    user_id: str = None
    is_active: bool = False

    def __post_init__(self):
        if self.user_id is None:
            self.user_id = str(uuid.uuid4())

    @classmethod
    def create(cls, username: str, email: str, password: str) -> 'User':
        """Create a new user with hashed password"""
        email_vo = Email(email)
        password_hash = cls._hash_password(password)
        return cls(
            username=username,
            email=email_vo,
            password_hash=password_hash
        )

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == self._hash_password(password)
