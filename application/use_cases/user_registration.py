from typing import Optional
from domain.entities.user import User
from application.interfaces.user_repository import UserRepository
from application.interfaces.email_service import EmailService
from application.dtos.user_dto import UserInputDTO, UserOutputDTO, user_entity_to_dto

class UserRegistrationUseCase:
    def __init__(self, user_repository: UserRepository, email_service: EmailService):
        self.user_repository = user_repository
        self.email_service = email_service

    def excute(self, input_dto: UserInputDTO) -> Optional[UserOutputDTO]:
        existing_user = self.user_repository.get_by_email(input_dto.email)
        if existing_user:
            raise ValueError(f"User with email {input_dto.email} already exists")

        # create new user
        user = User.create(
            username=input_dto.username,
            email=input_dto.email,
            password=input_dto.password
        )

        # save user to the database
        saved_user = self.user_repository.save(user)

        # send welcome email to the user
        self._send_welcome_email(saved_user)

        # return output DTO
        return user_entity_to_dto(saved_user)
    
    def _send_welcome_email(self, user: User) -> None:
        subject = "welcome to our platform"
        body = f"Hi {user.username},\n\nThank you for registering with us!"
        self.email_service.send_email(
            to_email=user.email.value,
            subject=subject,
            body=body
        )
