from fastapi import FastAPI, Depends, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud, schemas
from database import Base, engine, SessionLocal
from models import OCRResult
from ocr_service import extract_text_from_image

# Создаём таблицы в БД (если ещё не созданы)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OCR Microservice")

templates = Jinja2Templates(directory="templates")

# прописываем зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    # Получаем все результаты из БД
    results = crud.get_ocr_results(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": results
    })

@app.get("/upload", response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/ocr/upload")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Проверяем, что это точно изображение, а не посторонний файл. Ставим отбойник-заглушку если файл не подходит
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл не является изображением")

    # Читаем сам файл
    contents = await file.read()

    # Распознаём текст. проверить функцию(?)
    text = extract_text_from_image(contents)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Текст на изображении не распознан")

    # Создаём запись в БД
    ocr_data = schemas.OCRResultCreate(
        filename=file.filename,
        recognized_text=text
    )
    saved_record = crud.create_ocr_result(db, ocr_data)

    # Возвращаем JSON с результатом(3 парам)
    return {
        "id": saved_record.id,
        "filename": saved_record.filename,
        "recognized_text": saved_record.recognized_text
    }

@app.get("/details/{ocr_id}", response_class=HTMLResponse)
def get_ocr_details(
    ocr_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    result = crud.get_ocr_result(db, ocr_id)
    if not result:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    # Рендерим страничку
    return templates.TemplateResponse("details.html", {
        "request": request,
        "result": result
    })
# обязательно проверить работу Tesseract. предваритлеьно нужно прописать в системе Path.
# Создай отдельно для проверки перед запуском import os
# os.system("tesseract --version"). Если FOUND и exit code 0 - всё норм. прописался в Path.