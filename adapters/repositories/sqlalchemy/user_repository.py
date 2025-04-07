from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from application.interfaces.user_repository import UserRepository
from frameworks.database.models.user import UserModel
from sqlalchemy import select
import uuid

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> User:
        """Save a user to the database
        
        Args:
            user: User entity to save
            
        Returns:
            User: Saved user with generated ID
        """
        user_model = UserModel(
            id=str(uuid.uuid4()),
            username=user.username,
            email=user.email.value,
            password_hash=user.password.value
        )
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return User(
            user_id=str(user_model.id),
            username=user_model.username,
            email=Email(user_model.email),
            password=Password(user_model.password_hash)
        )

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID
        
        Args:
            user_id: User ID to find
            
        Returns:
            Optional[User]: Found user or None
        """
        user_model = await self.session.get(UserModel, user_id)
        if user_model is None:
            return None
        return User(
            user_id=str(user_model.id),
            username=user_model.username,
            email=Email(user_model.email),
            password=Password(user_model.password_hash)
        )

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email
        
        Args:
            email: Email to find
            
        Returns:
            Optional[User]: Found user or None
        """
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        if user_model is None:
            return None
        return User(
            user_id=str(user_model.id),
            username=user_model.username,
            email=Email(user_model.email),
            password=Password(user_model.password_hash)
        )

    async def get_all(self) -> List[User]:
        """Get all users
        
        Returns:
            List[User]: List of all users
        """
        result = await self.session.execute(select(UserModel))
        user_models = result.scalars().all()
        return [
            User(
                user_id=str(user_model.id),
                username=user_model.username,
                email=Email(user_model.email),
                password=Password(user_model.password_hash)
            )
            for user_model in user_models
        ]

    async def delete(self, user_id: str) -> User:
        """Delete a user by ID
        
        Args:
            user_id: User ID to delete
            
        Returns:
            User: Deleted user
            
        Raises:
            ValueError: If user not found
        """
        user_model = await self.session.get(UserModel, user_id)
        if user_model is None:
            raise ValueError(f"User with ID {user_id} not found")
        await self.session.delete(user_model)
        await self.session.commit()
        return User(
            user_id=str(user_model.id),
            username=user_model.username,
            email=Email(user_model.email),
            password=Password(user_model.password_hash)
        )