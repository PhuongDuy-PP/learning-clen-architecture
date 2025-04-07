from flask import Flask
from config.settings import DEBUG, SECRET_KEY
from frameworks.db.sqlalchemy_db import get_session
from frameworks.services.email_service import SMTPEmailService
from adapters.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository
from adapters.controllers.user_controller import UserController
from adapters.presenters.user_presenter import UserPresenter
from application.use_cases.user_registration import UserRegistrationUseCase
from frameworks.web.flask.routes import register_routes


def create_app(testing=False):
    """
    Create and configure the Flask application

    Args:
        testing: Whether the app is being created for testing

    Returns:
        Flask application instance
    """
    app = Flask(__name__)

    # Configure app
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG

    if not testing:
        # Setup dependencies for production use
        setup_dependencies(app)

    return app


def setup_dependencies(app):
    """
    Set up and wire dependencies for the application

    Args:
        app: Flask application instance
    """
    # Database session
    session = get_session()

    # Repositories
    user_repository = SQLAlchemyUserRepository(session)

    # Services
    email_service = SMTPEmailService()

    # Use cases
    user_registration_use_case = UserRegistrationUseCase(user_repository, email_service)

    # Presenters
    user_presenter = UserPresenter()

    # Controllers
    user_controller = UserController(
        user_registration_use_case=user_registration_use_case,
        user_presenter=user_presenter,
    )

    # Register routes
    register_routes(app, user_controller)


# If using gunicorn, this is needed
app = create_app()

if __name__ == "__main__":
    # Only for development server
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
