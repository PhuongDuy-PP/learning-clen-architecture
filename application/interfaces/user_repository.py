from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID
        
        Args:
            user_id: User ID to find
            
        Returns:
            Optional[User]: Found user or None
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email
        
        Args:
            email: Email to find
            
        Returns:
            Optional[User]: Found user or None
        """
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        """Get all users
        
        Returns:
            List[User]: List of all users
        """
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        """Save a user to the repository
        
        Args:
            user: User entity to save
            
        Returns:
            User: Saved user with generated ID
        """
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> User:
        """Delete a user by ID
        
        Args:
            user_id: User ID to delete
            
        Returns:
            User: Deleted user
            
        Raises:
            ValueError: If user not found
        """
        pass
