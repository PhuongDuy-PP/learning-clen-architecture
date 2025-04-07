from typing import Any, Dict
import re
from application.interfaces.validator import Validator
from domain.exceptions import InvalidEmailException, InvalidPasswordException, InvalidUsernameException
from application.dtos.user_dto import UserInputDTO

class UserValidator(Validator):
    def validate(self, data: Dict[str, Any]) -> None:
        """
        Validate user data
        
        Args:
            data: Dictionary containing user data
            
        Raises:
            InvalidUsernameException: If username is invalid
            InvalidEmailException: If email is invalid
            InvalidPasswordException: If password is invalid
        """
        if "username" in data:
            self._validate_username(data["username"])
        
        if "email" in data:
            self._validate_email(data["email"])
        
        if "password" in data:
            self._validate_password(data["password"])
    
    def _validate_username(self, username: str) -> None:
        """Validate username"""
        if not username or len(username) < 3 or len(username) > 50:
            raise InvalidUsernameException(
                "Username must be between 3 and 50 characters"
            )
        
        if not re.match("^[a-zA-Z0-9_-]+$", username):
            raise InvalidUsernameException(
                "Username can only contain letters, numbers, underscores and hyphens"
            )
    
    def _validate_email(self, email: str) -> None:
        """Validate email"""
        if not email:
            raise InvalidEmailException("Email is required")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise InvalidEmailException("Invalid email format")
    
    def _validate_password(self, password: str) -> None:
        """Validate password"""
        if not password:
            raise InvalidPasswordException("Password is required")
        
        if len(password) < 8:
            raise InvalidPasswordException(
                "Password must be at least 8 characters long"
            )
        
        if not re.search(r'[A-Z]', password):
            raise InvalidPasswordException(
                "Password must contain at least one uppercase letter"
            )
        
        if not re.search(r'[a-z]', password):
            raise InvalidPasswordException(
                "Password must contain at least one lowercase letter"
            )
        
        if not re.search(r'\d', password):
            raise InvalidPasswordException(
                "Password must contain at least one number"
            )

    def validate_user_input(self, user_input: UserInputDTO) -> None:
        """Validate user input data
        
        Args:
            user_input: User input data to validate
            
        Raises:
            ValueError: If validation fails
        """
        # Check required fields
        if not user_input.username:
            raise ValueError("Username is required")
        if not user_input.email:
            raise ValueError("Email is required")
        if not user_input.password:
            raise ValueError("Password is required")
            
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, user_input.email):
            raise ValueError("Invalid email format")
            
        # Validate password strength
        if len(user_input.password) < 8:
            raise ValueError("Password must be at least 8 characters long")
            
        # Validate username format
        if not user_input.username.isalnum():
            raise ValueError("Username must contain only letters and numbers") 