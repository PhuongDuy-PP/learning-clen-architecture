from typing import Dict, Any, Tuple
from application.use_cases.user_registration import UserRegistrationUseCase
from application.dtos.user_dto import UserInputDTO
from adapters.presenters.user_presenter import UserPresenter


class UserController:
    def __init__(
        self,
        user_registration_use_case: UserRegistrationUseCase,
        user_presenter: UserPresenter,
    ):
        self.user_registration_use_case = user_registration_use_case
        self.user_presenter = user_presenter

    def register_user(self, request_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
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
            output_dto = self.user_registration_use_case.execute(input_dto)

            # Use presenter to format the response
            user_data = self.user_presenter.present_user_for_api(output_dto)

            # Return response
            return {"success": True, "data": user_data}, 201

        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception as e:
            return {"success": False, "message": f"Server error: {str(e)}"}, 500

    def list_users(self) -> Tuple[Dict[str, Any], int]:
        """
        List all users

        Returns:
            Tuple containing response data and status code
        """
        try:
            # This would require a ListUsers use case
            # For now, we'll return a placeholder
            return {
                "success": True,
                "message": "User listing is not implemented yet",
            }, 501
        except Exception as e:
            return {"success": False, "message": f"Server error: {str(e)}"}, 500

    def get_user(self, user_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Get a user by ID

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            Tuple containing response data and status code
        """
        try:
            # This would require a GetUser use case
            # For now, we'll return a placeholder
            return {
                "success": True,
                "message": f"Getting user {user_id} is not implemented yet",
            }, 501
        except Exception as e:
            return {"success": False, "message": f"Server error: {str(e)}"}, 500

    def update_user(
        self, user_id: str, request_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], int]:
        """
        Update a user

        Args:
            user_id: The ID of the user to update
            request_data: JSON data from the request

        Returns:
            Tuple containing response data and status code
        """
        try:
            # This would require an UpdateUser use case
            # For now, we'll return a placeholder
            return {
                "success": True,
                "message": f"Updating user {user_id} is not implemented yet",
            }, 501
        except Exception as e:
            return {"success": False, "message": f"Server error: {str(e)}"}, 500

    def delete_user(self, user_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Delete a user

        Args:
            user_id: The ID of the user to delete

        Returns:
            Tuple containing response data and status code
        """
        try:
            # This would require a DeleteUser use case
            # For now, we'll return a placeholder
            return {
                "success": True,
                "message": f"Deleting user {user_id} is not implemented yet",
            }, 501
        except Exception as e:
            return {"success": False, "message": f"Server error: {str(e)}"}, 500
