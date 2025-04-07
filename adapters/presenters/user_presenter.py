from typing import Dict, Any
from application.dtos.user_dto import UserOutputDTO


class UserPresenter:
    """
    Presenter for transforming UserOutputDTO to different formats based on the client needs.
    This is part of the Interface Adapters layer in Clean Architecture.
    """

    @staticmethod
    def present_user_for_api(user_dto: UserOutputDTO) -> Dict[str, Any]:
        """
        Transform UserOutputDTO to a dictionary format suitable for API responses

        Args:
            user_dto: The output DTO from a use case

        Returns:
            Dict: User data formatted for API response
        """
        return {
            "id": user_dto.user_id,
            "username": user_dto.username,
            "email": user_dto.email,
            "is_active": user_dto.is_active,
            # Additional fields could be added here as needed
        }

    @staticmethod
    def present_user_list_for_api(
        user_dtos: list[UserOutputDTO],
    ) -> list[Dict[str, Any]]:
        """
        Transform a list of UserOutputDTO to a list of dictionaries for API responses

        Args:
            user_dtos: List of output DTOs from a use case

        Returns:
            List[Dict]: List of user data formatted for API response
        """
        return [UserPresenter.present_user_for_api(user_dto) for user_dto in user_dtos]

    @staticmethod
    def present_user_for_web(user_dto: UserOutputDTO) -> Dict[str, Any]:
        """
        Transform UserOutputDTO to a format suitable for web templates

        Args:
            user_dto: The output DTO from a use case

        Returns:
            Dict: User data formatted for web presentation
        """
        return {
            "id": user_dto.user_id,
            "username": user_dto.username,
            "email": user_dto.email,
            "is_active": "Active" if user_dto.is_active else "Inactive",
            "profile_url": f"/users/{user_dto.user_id}",
            # Additional fields could be added here as needed for web display
        }
