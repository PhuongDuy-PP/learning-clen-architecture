from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from application.interfaces.user_repository import UserRepository
from frameworks.logging.logger import FileLogger
from application.validators.user_validator import UserValidator
from application.dtos.user_dto import UserUpdateDTO

class UpdateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        logger: FileLogger,
        validator: UserValidator
    ):
        self.user_repository = user_repository
        self.logger = logger
        self.validator = validator

    async def execute(self, user_id: str, input_dto: UserUpdateDTO) -> User:
        """Update a user
        
        Args:
            user_id: User ID to update
            input_dto: User update data
            
        Returns:
            User: Updated user
            
        Raises:
            ValueError: If user not found or validation fails
        """
        # Get existing user
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            self.logger.error(f"User with ID {user_id} not found")
            raise ValueError(f"User with ID {user_id} not found")

        # Validate updated data
        validation_data = {}
        if input_dto.email is not None:
            validation_data["email"] = input_dto.email
        if input_dto.username is not None:
            validation_data["username"] = input_dto.username
        self.validator.validate(validation_data)

        # Update user fields
        updated_user = User(
            user_id=user_id,
            username=input_dto.username or existing_user.username,
            email=Email(input_dto.email or existing_user.email.value),
            password=existing_user.password
        )

        # Save updated user
        saved_user = await self.user_repository.save(updated_user)
        self.logger.info(f"User {user_id} updated successfully")
        return saved_user 