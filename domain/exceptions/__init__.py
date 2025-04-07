class InvalidEmailException(Exception):
    """Exception raised when email is invalid"""
    pass

class InvalidPasswordException(Exception):
    """Exception raised when password is invalid"""
    pass

class InvalidUsernameException(Exception):
    """Exception raised when username is invalid"""
    pass

class UserNotFoundException(Exception):
    """Exception raised when user is not found"""
    pass

class UserAlreadyExistsException(Exception):
    """Exception raised when user already exists"""
    pass 