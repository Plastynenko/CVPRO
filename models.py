from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

# Модель таблицы (SQLAlchemy)
class OCRResult(Base):
    __tablename__ = "ocr_results"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    recognized_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
