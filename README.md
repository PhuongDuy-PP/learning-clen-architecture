my_clean_app/
├── domain/                  # Entities + Business Rules
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── user.py
│   └── value_objects/
│       ├── __init__.py
│       └── email.py
│
├── application/             # Use Cases
│   ├── __init__.py
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── email_service.py
│   ├── use_cases/
│   │   ├── __init__.py
│   │   ├── user_registration.py
│   │   └── user_authentication.py
│   └── dtos/
│       ├── __init__.py
│       └── user_dto.py
│
├── adapters/                # Interface Adapters
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── user_controller.py
│   ├── presenters/
│   │   ├── __init__.py
│   │   └── user_presenter.py
│   └── repositories/
│       ├── __init__.py
│       ├── sqlalchemy/
│       │   ├── __init__.py
│       │   ├── models.py 
│       │   └── user_repository.py
│       └── mongodb/
│           ├── __init__.py
│           └── user_repository.py
│
├── frameworks/              # Frameworks & Drivers
│   ├── __init__.py
│   ├── web/
│   │   ├── __init__.py
│   │   ├── flask/
│   │   │   ├── __init__.py
│   │   │   ├── app.py
│   │   │   └── routes.py
│   │   └── fastapi/
│   │       ├── __init__.py
│   │       ├── app.py
│   │       └── routes.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── sqlalchemy_db.py
│   │   └── mongodb_client.py
│   └── services/
│       ├── __init__.py
│       └── email_service.py
│
├── config/                  # Configuration
│   ├── __init__.py
│   └── settings.py
│
├── main.py                  # Application entry point
└── requirements.txt