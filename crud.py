from sqlalchemy.orm import Session
from models import OCRResult
from schemas import OCRResultCreate

def create_ocr_result(db: Session, ocr_result: OCRResultCreate):
    db_ocr = OCRResult(
        filename=ocr_result.filename,
        recognized_text=ocr_result.recognized_text
    )
    db.add(db_ocr)
    db.commit()
    db.refresh(db_ocr)
    return db_ocr

def get_ocr_result(db: Session, ocr_id: int):
    return db.query(OCRResult).filter(OCRResult.id == ocr_id).first()

def get_ocr_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(OCRResult).offset(skip).limit(limit).all()
#провеврить зависимости!