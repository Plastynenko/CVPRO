import pytesseract
from PIL import Image
import io

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Принимает байты изображения, возвращает распознанный текст (Tesseract).
    """
    image = Image.open(io.BytesIO(image_bytes))
    # Укажите нужные языки: 'eng', 'rus' или 'eng+rus'
    text = pytesseract.image_to_string(image, lang='eng+rus')
    return text.strip()
