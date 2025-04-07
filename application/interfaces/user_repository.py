from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by their ID"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email"""
        pass

    @abstractmethod
    def list(self) -> List[User]:
        """List all users"""
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Save a user"""
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """Delete a user by their ID"""
        pass
