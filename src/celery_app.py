import os

from PIL import Image
import pytesseract
from fastapi import HTTPException
from celery import Celery

from src.database import session_
from src.models.models import Documents_text

# from src.main import path_to_doc, app_dir
app_dir = os.path.dirname(__file__)  # сохраняем в отдельную переменную

celery_app = Celery("tasks", backend="redis://localhost", broker="redis://localhost")
# celery -A src.celery_app worker --loglevel=INFO


@celery_app.task
def scan(image: str, doc_id=int) -> None:
    """
    :decription: Распознавание текста тессерактом, его добавление в БД
    :param image: путь к файлу
    :param doc_id: id в БД"""
    try:
        image = Image.open(image)
        string = pytesseract.image_to_string(image, lang="rus")
        # Добавление в БД
        with session_() as session:
            text_to_db = Documents_text(id_doc=doc_id, text=string)
            session.add(text_to_db)
            session.commit()

    except:
        return None
