from abc import ABC, abstractmethod
from typing import Any, Dict
from application.dtos.user_dto import UserInputDTO

class Validator(ABC):
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> None:
        """
        Validate the input data
        
        Args:
            data: Dictionary containing the data to validate
            
        Raises:
            ValidationError: If validation fails
        """
        pass

    @abstractmethod
    def validate_user_input(self, user_input: UserInputDTO) -> None:
        """Validate user input data
        
        Args:
            user_input: User input data to validate
            
        Raises:
            ValueError: If validation fails
        """
        pass 