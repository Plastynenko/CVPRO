from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# База данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./ocr_results.db"

# Создаём движок
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()