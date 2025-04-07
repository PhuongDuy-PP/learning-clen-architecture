from typing import Optional
from domain.entities.user import User
from application.interfaces.user_repository import UserRepository
from frameworks.logging.logger import FileLogger

class GetUserUseCase:
    def __init__(self, user_repository: UserRepository, logger: FileLogger):
        self.user_repository = user_repository
        self.logger = logger

    async def execute(self, user_id: str) -> Optional[User]:
        """Get a user by ID
        
        Args:
            user_id: User ID to find
            
        Returns:
            Optional[User]: Found user or None
        """
        self.logger.info(f"Getting user with ID: {user_id}")
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            self.logger.warning(f"User with ID {user_id} not found")
        return user 