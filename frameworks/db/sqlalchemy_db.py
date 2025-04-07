from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config.settings import DATABASE_URL

# Tạo engine kết nối đến MySQL database
engine = create_engine(
    DATABASE_URL,
    pool_size=10,  # Kích thước pool connection
    max_overflow=20,  # Số lượng connection tối đa có thể vượt quá pool_size
    pool_recycle=3600,  # Thời gian tái sử dụng connection (tránh "MySQL server has gone away")
    pool_pre_ping=True,  # Kiểm tra connection trước khi sử dụng
    echo=False,  # Set True để hiển thị SQL queries (khi debug)
)

# Tạo factory cho session
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tạo scoped session để thread-safe
Session = scoped_session(session_factory)

# Base class cho các models
Base = declarative_base()


def get_session():
    """
    Get a new database session

    Returns:
        SQLAlchemy session
    """
    db = Session()
    try:
        return db
    finally:
        # Đảm bảo session được đóng sau khi return
        db.close()


def init_db():
    """
    Initialize the database, create all tables
    """
    # Import all models to ensure they are registered with Base
    from adapters.repositories.sqlalchemy.models import UserModel  # noqa

    # Create all tables
    Base.metadata.create_all(bind=engine)
