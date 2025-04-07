# Dự Án Python Áp Dụng Clean Architecture

Dự án này minh họa việc triển khai Clean Architecture trong Python, tập trung vào chức năng quản lý người dùng.

## Cấu Trúc Dự Án

```
.
├── adapters/                     # Lớp Interface Adapters
│   ├── controllers/             # Controllers xử lý HTTP requests
│   │   └── user_controller.py
│   ├── presenters/             # Presenters định dạng responses
│   │   └── user_presenter.py
│   └── repositories/           # Triển khai repositories
│       └── sqlalchemy/
│           └── user_repository.py
│
├── application/                 # Lớp Application Business Rules
│   ├── dtos/                  # Data Transfer Objects
│   │   └── user_dto.py
│   ├── interfaces/            # Định nghĩa interfaces
│   │   ├── email_service.py
│   │   └── user_repository.py
│   ├── use_cases/            # Use cases/dịch vụ ứng dụng
│   │   ├── delete_user.py
│   │   ├── get_user.py
│   │   ├── list_users.py
│   │   ├── update_user.py
│   │   └── user_registration.py
│   └── validators/           # Logic xác thực
│       └── user_validator.py
│
├── domain/                     # Lớp Enterprise Business Rules
│   ├── entities/             # Business entities
│   │   └── user.py
│   ├── exceptions/           # Domain exceptions
│   │   └── domain_exception.py
│   ├── value_objects/        # Value objects
│   │   ├── email.py
│   │   └── password.py
│   └── models/              # Domain models
│
├── frameworks/                 # Lớp Frameworks & Drivers
│   ├── container/           # Dependency injection container
│   │   └── container.py
│   ├── database/           # Cấu hình và models database
│   │   ├── database.py
│   │   └── models/
│   │       └── user.py
│   ├── email/             # Triển khai dịch vụ email
│   │   └── email_service.py
│   ├── logging/          # Cấu hình logging
│   │   └── logger.py
│   ├── services/        # Dịch vụ bên ngoài
│   └── web/            # Cấu hình framework web
│
├── tests/                    # Thư mục test
│   ├── mocks/             # Mock objects cho testing
│   └── test_user.py      # Tests liên quan đến user
│
├── alembic/                 # Database migrations
│   └── versions/
│       └── recreate_users_table.py
│
├── config/                  # Các file cấu hình
│   └── settings.py
│
├── static/                  # Các file tĩnh
│   └── swagger.json       # Tài liệu API
│
├── .env                    # Biến môi trường
├── .gitignore             # Git ignore file
├── alembic.ini            # Cấu hình Alembic
├── app.py                 # Điểm vào của ứng dụng
├── requirements.txt       # Các dependency của dự án
└── README.md             # Tài liệu dự án
```

## Giải Thích Chi Tiết Cấu Trúc Thư Mục

### Lớp Domain (`domain/`)
Lớp Domain là lớp trong cùng của Clean Architecture, chứa logic nghiệp vụ cốt lõi của ứng dụng.

- **entities/**: Chứa các business entities đại diện cho các đối tượng cốt lõi trong hệ thống. Đây là phần ổn định nhất của ứng dụng và không phụ thuộc vào các lớp khác.
  - `user.py`: Định nghĩa entity User với các thuộc tính và quy tắc nghiệp vụ.

- **value_objects/**: Chứa các đối tượng bất biến đại diện cho các khái niệm trong domain. Khác với entities, value objects được xác định bởi thuộc tính của chúng thay vì danh tính.
  - `email.py`: Đại diện cho địa chỉ email với các quy tắc xác thực.
  - `password.py`: Đại diện cho mật khẩu với các quy tắc băm và xác thực.

- **exceptions/**: Chứa các exception đặc thù của domain được ném ra khi các quy tắc nghiệp vụ bị vi phạm.
  - `domain_exception.py`: Lớp exception cơ sở cho các lỗi đặc thù của domain.

- **models/**: Chứa các domain models đại diện cho các khái niệm nghiệp vụ một cách trừu tượng hơn so với entities.

### Lớp Application (`application/`)
Lớp Application chứa các quy tắc nghiệp vụ cụ thể của ứng dụng và điều phối luồng dữ liệu giữa các entities.

- **dtos/**: Chứa các Data Transfer Objects được sử dụng để truyền dữ liệu giữa các lớp.
  - `user_dto.py`: Định nghĩa các DTO cho các thao tác liên quan đến user (input, output, update).

- **interfaces/**: Chứa các định nghĩa interface để định nghĩa hợp đồng cho các phụ thuộc bên ngoài.
  - `email_service.py`: Interface cho dịch vụ email.
  - `user_repository.py`: Interface cho các thao tác repository của user.

- **use_cases/**: Chứa các quy tắc nghiệp vụ cụ thể và các use case.
  - `user_registration.py`: Xử lý logic đăng ký user.
  - `get_user.py`: Xử lý việc lấy thông tin user theo ID.
  - `list_users.py`: Xử lý việc liệt kê tất cả users.
  - `update_user.py`: Xử lý việc cập nhật thông tin user.
  - `delete_user.py`: Xử lý việc xóa user.

- **validators/**: Chứa logic xác thực dữ liệu ứng dụng.
  - `user_validator.py`: Xác thực dữ liệu liên quan đến user.

### Lớp Adapters (`adapters/`)
Lớp Adapters chứa các thành phần thích ứng các cơ quan bên ngoài với các use case của ứng dụng.

- **controllers/**: Chứa các controller xử lý các request và response HTTP.
  - `user_controller.py`: Xử lý các HTTP request liên quan đến user.

- **presenters/**: Chứa các presenter định dạng dữ liệu cho giao diện người dùng.
  - `user_presenter.py`: Định dạng dữ liệu user cho API responses.

- **repositories/**: Chứa các triển khai của các interface repository.
  - `sqlalchemy/user_repository.py`: Triển khai SQLAlchemy của user repository.

### Lớp Frameworks (`frameworks/`)
Lớp Frameworks chứa các framework, công cụ và các cơ quan bên ngoài mà ứng dụng tương tác.

- **container/**: Chứa cấu hình container dependency injection.
  - `container.py`: Cấu hình dependency injection cho ứng dụng.

- **database/**: Chứa cấu hình cơ sở dữ liệu và các model ORM.
  - `database.py`: Kết nối và cấu hình cơ sở dữ liệu.
  - `models/user.py`: Model SQLAlchemy cho entity User.

- **email/**: Chứa triển khai dịch vụ email.
  - `email_service.py`: Triển khai của interface dịch vụ email.

- **logging/**: Chứa cấu hình logging.
  - `logger.py`: Cấu hình logging cho ứng dụng.

- **services/**: Chứa tích hợp dịch vụ bên ngoài.
- **web/**: Chứa cấu hình framework web.

### Các Thư Mục Hỗ Trợ

- **tests/**: Chứa các file test cho ứng dụng.
  - `mocks/`: Chứa các mock objects cho testing.
  - `test_user.py`: Tests cho chức năng liên quan đến user.

- **alembic/**: Chứa các file migration cơ sở dữ liệu.
  - `versions/recreate_users_table.py`: Migration để tạo bảng users.

- **config/**: Chứa các file cấu hình.
  - `settings.py`: Cài đặt ứng dụng.

- **static/**: Chứa các file tĩnh.
  - `swagger.json`: Tài liệu API ở định dạng Swagger.

## Trách Nhiệm Của Các Lớp

### Lớp Domain
- Chứa các quy tắc nghiệp vụ doanh nghiệp
- Bao gồm entities, value objects và domain exceptions
- Độc lập với các lớp khác
- Không phụ thuộc vào frameworks hoặc thư viện

### Lớp Application
- Chứa các quy tắc nghiệp vụ cụ thể của ứng dụng
- Định nghĩa use cases và interfaces
- Chỉ phụ thuộc vào lớp domain
- Chứa DTOs để truyền dữ liệu

### Lớp Adapters
- Triển khai các interfaces được định nghĩa trong lớp application
- Chứa controllers, presenters và repositories
- Thích ứng các frameworks bên ngoài với ứng dụng
- Phụ thuộc vào lớp application và domain

### Lớp Frameworks
- Chứa frameworks và công cụ
- Triển khai các chi tiết kỹ thuật
- Bao gồm cấu hình database, email, logging
- Có nhiều phụ thuộc bên ngoài nhất

## Tính Năng Chính

- Triển khai Clean Architecture
- Hỗ trợ async/await
- SQLAlchemy với hỗ trợ async
- Dependency injection
- Tích hợp dịch vụ email
- Hệ thống logging
- Tài liệu API với Swagger
- Database migrations với Alembic

## Hướng Dẫn Bắt Đầu

1. Clone repository
2. Tạo môi trường ảo: `python -m venv venv`
3. Kích hoạt môi trường ảo:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Cài đặt dependencies: `pip install -r requirements.txt`
5. Thiết lập biến môi trường trong `.env`
6. Chạy migrations: `alembic upgrade head`
7. Khởi động ứng dụng: `python app.py`

## API Endpoints

- POST `/api/users/register` - Đăng ký người dùng mới
- GET `/api/users` - Liệt kê tất cả người dùng
- GET `/api/users/<user_id>` - Lấy thông tin người dùng theo ID
- PUT `/api/users/<user_id>` - Cập nhật thông tin người dùng
- DELETE `/api/users/<user_id>` - Xóa người dùng

## Testing

Chạy tests với:
```bash
pytest
```

## Đóng Góp

1. Fork repository
2. Tạo nhánh tính năng
3. Commit các thay đổi
4. Push lên nhánh
5. Tạo Pull Request