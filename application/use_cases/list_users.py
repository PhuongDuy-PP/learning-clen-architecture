from typing import List
from domain.entities.user import User
from application.interfaces.user_repository import UserRepository
from frameworks.logging.logger import FileLogger

class ListUsersUseCase:
    def __init__(self, user_repository: UserRepository, logger: FileLogger):
        self.user_repository = user_repository
        self.logger = logger

    async def execute(self) -> List[User]:
        """Get all users
        
        Returns:
            List[User]: List of all users
        """
        self.logger.info("Getting all users")
        users = await self.user_repository.get_all()
        self.logger.info(f"Found {len(users)} users")
        return users 