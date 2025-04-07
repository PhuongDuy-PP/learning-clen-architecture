# Clean Architecture API

A RESTful API built using Clean Architecture principles in Python with Flask.

## Project Structure

```
my_clean_app/
├── alembic/                    # Database migrations
├── domain/                     # Enterprise business rules
│   ├── entities/              # Business entities
│   │   └── user.py
│   └── value_objects/         # Value objects
│       └── email.py
│
├── application/               # Application business rules
│   ├── dtos/                 # Data Transfer Objects
│   │   └── user_dto.py
│   ├── interfaces/           # Repository interfaces
│   │   └── user_repository.py
│   └── use_cases/           # Use cases/interactors
│       ├── user_registration.py
│       ├── get_user.py
│       ├── list_users.py
│       ├── update_user.py
│       └── delete_user.py
│
├── adapters/                 # Interface adapters
│   ├── controllers/         # Controllers/presenters
│   │   └── user_controller.py
│   ├── presenters/         # Response formatters
│   │   └── user_presenter.py
│   └── repositories/       # Repository implementations
│       └── sqlalchemy/
│           ├── models.py
│           └── user_repository.py
│
├── frameworks/              # Frameworks and drivers
│   ├── database/          # Database configuration
│   │   ├── database.py
│   │   └── connection.py
│   └── email/            # Email service
│       └── email_service.py
│
├── tests/                 # Test directory
├── app.py                # Application entry point
├── requirements.txt      # Project dependencies
├── alembic.ini          # Alembic configuration
├── .env                 # Environment variables
└── README.md            # Project documentation
```

## Layer Description

1. **Domain Layer** (`domain/`)
   - Contains enterprise business rules
   - Independent of other layers
   - Includes entities and value objects
   - No dependencies on frameworks or external agencies

2. **Application Layer** (`application/`)
   - Contains application business rules
   - Defines interfaces for external dependencies
   - Orchestrates flow of data between entities
   - Implements use cases

3. **Adapters Layer** (`adapters/`)
   - Converts data between use cases and external agencies
   - Implements repository interfaces
   - Contains controllers and presenters
   - Handles data format transformation

4. **Frameworks Layer** (`frameworks/`)
   - Contains frameworks and tools
   - Database implementations
   - External services (email, etc.)
   - Web frameworks

## API Endpoints

### Users
- `POST /api/users/register` - Register a new user
- `GET /api/users` - List all users
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`
5. Initialize the database:
   ```bash
   alembic upgrade head
   ```
6. Run the application:
   ```bash
   python app.py
   ```

## Testing

Run tests using:
```bash
python -m pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request