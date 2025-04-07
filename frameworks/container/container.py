from dependency_injector import containers, providers
from application.use_cases.user_registration import UserRegistrationUseCase
from application.use_cases.get_user import GetUserUseCase
from application.use_cases.list_users import ListUsersUseCase
from application.use_cases.update_user import UpdateUserUseCase
from application.use_cases.delete_user import DeleteUserUseCase
from adapters.controllers.user_controller import UserController
from adapters.presenters.user_presenter import UserPresenter
from adapters.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository
from frameworks.database.database import get_db, init_db
from frameworks.email.email_service import SMTPEmailService
from frameworks.logging.logger import FileLogger
from application.validators.user_validator import UserValidator

class Container(containers.DeclarativeContainer):
    # Configuration
    config = providers.Configuration()
    
    # Database
    database = providers.Resource(
        init_db
    )
    
    # Repositories
    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        session=providers.Resource(get_db)
    )
    
    # Services
    email_service = providers.Singleton(
        SMTPEmailService
    )
    
    logger = providers.Singleton(
        FileLogger,
        name="clean_architecture",
        log_file="app.log"
    )
    
    # Validators
    user_validator = providers.Singleton(
        UserValidator
    )
    
    # Use cases
    user_registration_use_case = providers.Factory(
        UserRegistrationUseCase,
        user_repository=user_repository,
        email_service=email_service,
        logger=logger,
        validator=user_validator
    )
    
    get_user_use_case = providers.Factory(
        GetUserUseCase,
        user_repository=user_repository,
        logger=logger
    )
    
    list_users_use_case = providers.Factory(
        ListUsersUseCase,
        user_repository=user_repository,
        logger=logger
    )
    
    update_user_use_case = providers.Factory(
        UpdateUserUseCase,
        user_repository=user_repository,
        logger=logger,
        validator=user_validator
    )
    
    delete_user_use_case = providers.Factory(
        DeleteUserUseCase,
        user_repository=user_repository,
        logger=logger
    )
    
    # Presenters
    user_presenter = providers.Singleton(
        UserPresenter
    )
    
    # Controllers
    user_controller = providers.Factory(
        UserController,
        user_registration_use_case=user_registration_use_case,
        get_user_use_case=get_user_use_case,
        list_users_use_case=list_users_use_case,
        update_user_use_case=update_user_use_case,
        delete_user_use_case=delete_user_use_case,
        user_presenter=user_presenter,
        logger=logger
    ) 