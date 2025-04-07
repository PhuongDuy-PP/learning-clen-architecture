from typing import Optional
from domain.entities.user import User
from application.interfaces.user_repository import UserRepository
from application.interfaces.email_service import EmailService
from frameworks.logging.logger import FileLogger
from application.validators.user_validator import UserValidator
from application.dtos.user_dto import UserInputDTO, UserOutputDTO, user_entity_to_dto

class UserRegistrationUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        email_service: EmailService,
        logger: FileLogger,
        validator: UserValidator
    ):
        self.user_repository = user_repository
        self.email_service = email_service
        self.logger = logger
        self.validator = validator

    async def execute(self, input_dto: UserInputDTO) -> User:
        """Register a new user
        
        Args:
            input_dto: User input data
            
        Returns:
            User: Registered user
            
        Raises:
            ValueError: If validation fails
        """
        # Validate user data
        self.validator.validate({
            "username": input_dto.username,
            "email": input_dto.email,
            "password": input_dto.password
        })
        
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(input_dto.email)
        if existing_user:
            raise ValueError("User with this email already exists")
            
        # Create user
        user = User.create(
            username=input_dto.username,
            email=input_dto.email,
            password=input_dto.password
        )
        
        # Save user
        saved_user = await self.user_repository.save(user)
        
        # Send welcome email
        self.email_service.send_email(
            to_email=saved_user.email,
            subject="Welcome to Clean Architecture",
            body=f"Welcome {saved_user.username}! Your account has been created."
        )
        
        self.logger.info(f"User {saved_user.username} registered successfully")
        
        return saved_user

    def _send_welcome_email(self, user: User) -> None:
        subject = "welcome to our platform"
        body = f"Hi {user.username},\n\nThank you for registering with us!"
        try:
            self.email_service.send_email(
                to_email=user.email.value,
                subject=subject,
                body=body
            )
            self.logger.info(f"Welcome email sent to user: {user.email.value}")
        except Exception as e:
            self.logger.error(f"Failed to send welcome email to {user.email.value}: {str(e)}")
