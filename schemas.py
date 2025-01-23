from pydantic import BaseModel
from datetime import datetime

# Здесь представлена базовая схема
class OCRResultBase(BaseModel):
    filename: str
    recognized_text: str

# Схема для создания записи
class OCRResultCreate(OCRResultBase):
    pass

# Схема для чтения/возврата из БД (для Pydantic 2ой версии. проверить синткасис)
class OCRResultInDB(OCRResultBase):
    id: int
    created_at: datetime

    class Config:
        # Внимание, синт-с! В Pydantic v2 вместо orm_mode=True используем from_attributes=True
        from_attributes = True
