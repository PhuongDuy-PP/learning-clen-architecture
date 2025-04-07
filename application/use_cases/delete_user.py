from domain.entities.user import User
from application.interfaces.user_repository import UserRepository
from frameworks.logging.logger import FileLogger

class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository, logger: FileLogger):
        self.user_repository = user_repository
        self.logger = logger

    async def execute(self, user_id: str) -> User:
        """Delete a user
        
        Args:
            user_id: User ID to delete
            
        Returns:
            User: Deleted user
            
        Raises:
            ValueError: If user not found
        """
        self.logger.info(f"Deleting user with ID: {user_id}")
        deleted_user = await self.user_repository.delete(user_id)
        self.logger.info(f"User {user_id} deleted successfully")
        return deleted_user 