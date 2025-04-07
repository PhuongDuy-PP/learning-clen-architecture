from dataclasses import dataclass
from typing import Optional
from domain.entities.user import User

@dataclass
class UserInputDTO:
    username: str
    email: str
    password: str

@dataclass
class UserUpdateDTO:
    username: Optional[str] = None
    email: Optional[str] = None

@dataclass
class UserOutputDTO:
    user_id: str
    username: str
    email: str
    is_active: bool

def user_entity_to_dto(user: User) -> UserOutputDTO:
    return UserOutputDTO(
        user_id=user.user_id,
        username=user.username,
        email=str(user.email),
        is_active=user.is_active
    )