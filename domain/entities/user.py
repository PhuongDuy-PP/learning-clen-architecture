from dataclasses import dataclass
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from typing import Optional
import hashlib
import uuid

@dataclass
class User:
    user_id: str
    username: str
    email: Email
    password: Password
    is_active: bool = True

    def __post_init__(self):
        if self.user_id is None:
            self.user_id = str(uuid.uuid4())

    @classmethod
    def create(cls, username: str, email: str, password: str) -> 'User':
        """Create a new user with hashed password"""
        return cls(
            user_id=str(uuid.uuid4()),
            username=username,
            email=Email(email),
            password=Password(password),
            is_active=True
        )

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == self._hash_password(password)

    def update(self, username: str, email: str, password: str) -> None:
        self.username = username
        self.email = Email(email)
        self.password = Password(password)
