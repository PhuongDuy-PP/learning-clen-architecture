from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.user import User
from domain.value_objects.email import Email
from application.interfaces.user_repository import UserRepository
from adapters.repositories.sqlalchemy.models import UserModel

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, user_id: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            return None
        return self._model_to_entity(user_model)
    
    def get_by_email(self, email: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter(UserModel.email == email).first()
        if not user_model:
            return None
        return self._model_to_entity(user_model)
    
    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            user_id=model.id,
            username=model.username,
            email=Email(model.email),
            password_hash=model.password_hash,
            is_active=model.is_active
        )