from typing import Dict, Any, Tuple
from application.use_cases.user_registration import UserRegistrationUseCase
from application.use_cases.get_user import GetUserUseCase
from application.use_cases.list_users import ListUsersUseCase
from application.use_cases.update_user import UpdateUserUseCase
from application.use_cases.delete_user import DeleteUserUseCase
from application.dtos.user_dto import UserInputDTO, UserUpdateDTO, UserOutputDTO, user_entity_to_dto
from adapters.presenters.user_presenter import UserPresenter
from frameworks.logging.logger import FileLogger


class UserController:
    def __init__(
        self,
        user_registration_use_case: UserRegistrationUseCase,
        get_user_use_case: GetUserUseCase,
        list_users_use_case: ListUsersUseCase,
        update_user_use_case: UpdateUserUseCase,
        delete_user_use_case: DeleteUserUseCase,
        user_presenter: UserPresenter,
        logger: FileLogger
    ):
        self.user_registration_use_case = user_registration_use_case
        self.get_user_use_case = get_user_use_case
        self.list_users_use_case = list_users_use_case
        self.update_user_use_case = update_user_use_case
        self.delete_user_use_case = delete_user_use_case
        self.user_presenter = user_presenter
        self.logger = logger

    async def register_user(self, request_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        Register a new user

        Args:
            request_data: JSON data from the request

        Returns:
            Tuple containing response data and status code
        """
        try:
            # Validate request data
            if not all(
                key in request_data for key in ["username", "email", "password"]
            ):
                return {"success": False, "message": "Missing required fields"}, 400

            # Create input DTO
            input_dto = UserInputDTO(
                username=request_data["username"],
                email=request_data["email"],
                password=request_data["password"],
            )

            # Execute use case
            output_dto = await self.user_registration_use_case.execute(input_dto)

            # Use presenter to format the response
            user_data = self.user_presenter.present_user_for_api(output_dto)

            # Return response
            return {"success": True, "data": user_data}, 201

        except ValueError as e:
            self.logger.error(f"User registration failed: {str(e)}")
            return {"success": False, "message": str(e)}, 400
        except Exception as e:
            self.logger.error(f"Server error: {str(e)}")
            return {"success": False, "message": f"Server error: {str(e)}"}, 500

    async def list_users(self) -> Tuple[Dict[str, Any], int]:
        """
        List all users

        Returns:
            Tuple containing response data and status code
        """
        try:
            # Execute use case
            users = await self.list_users_use_case.execute()
            
            # Use presenter to format the response
            users_data = [self.user_presenter.present_user_for_api(user) for user in users]
            
            return {
                "success": True,
                "data": users_data
            }, 200
        except Exception as e:
            self.logger.error(f"Error listing users: {str(e)}")
            return {"success": False, "message": f"Server error: {str(e)}"}, 500

    async def get_user(self, user_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Get a user by ID

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            Tuple containing response data and status code
        """
        try:
            # Execute use case
            user = await self.get_user_use_case.execute(user_id)
            
            if user is None:
                return {"success": False, "message": "User not found"}, 404
            
            # Convert User entity to UserOutputDTO using helper function
            user_dto = user_entity_to_dto(user)
            
            # Use presenter to format the response
            user_data = self.user_presenter.present_user_for_api(user_dto)
            
            return {
                "success": True,
                "data": user_data
            }, 200
        except Exception as e:
            self.logger.error(f"Error getting user: {str(e)}")
            return {"success": False, "message": str(e)}, 500

    async def update_user(self, user_id: str, request_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        Update a user

        Args:
            user_id: The ID of the user to update
            request_data: JSON data from the request

        Returns:
            Tuple containing response data and status code
        """
        try:
            # Create input DTO
            input_dto = UserUpdateDTO(
                username=request_data.get("username"),
                email=request_data.get("email")
            )

            # Execute use case
            updated_user = await self.update_user_use_case.execute(user_id, input_dto)
            
            # Use presenter to format the response
            user_data = self.user_presenter.present_user_for_api(updated_user)
            
            return {
                "success": True,
                "data": user_data
            }, 200
        except ValueError as e:
            self.logger.error(f"User update failed: {str(e)}")
            return {"success": False, "message": str(e)}, 404
        except Exception as e:
            self.logger.error(f"Server error: {str(e)}")
            return {"success": False, "message": f"Server error: {str(e)}"}, 500

    async def delete_user(self, user_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Delete a user

        Args:
            user_id: The ID of the user to delete

        Returns:
            Tuple containing response data and status code
        """
        try:
            # Execute use case
            user = await self.delete_user_use_case.execute(user_id)
            
            return {
                "success": True,
                "message": "User deleted successfully"
            }, 200
        except ValueError as e:
            self.logger.error(f"User deletion failed: {str(e)}")
            return {"success": False, "message": str(e)}, 404
        except Exception as e:
            self.logger.error(f"Server error: {str(e)}")
            return {"success": False, "message": f"Server error: {str(e)}"}, 500
