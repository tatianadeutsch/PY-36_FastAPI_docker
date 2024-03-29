import os

from PIL import Image
import pytesseract
from celery import Celery

from database import session_
from models import Documents_text
from configs import REDIS_HOST, REDIS_PORT

# from src.main import path_to_doc, app_dir
app_dir = os.path.dirname(__file__)  # сохраняем в отдельную переменную

celery_app = Celery(
    "tasks",
    # backend=f"redis://localhost",
    # broker=f"redis://localhost",
    # для докера, иначе не разворачивается!!!
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    broker_connection_retry_on_startup=True,
)
# celery -A src.celery_app:celery_app worker --loglevel=INFO # --pool=solo - для винды
# celery -A src.celery_app:celery_app flower - запуск визуализации процессов
# http://localhost:5555/ - вход на сервер селери flower


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


# print(
#     scan(
#         "/home/nepogoda/PycharmProjects/pythonProject/documents/a0e1e55c-c907-4c3c-9882-088cc1f35bd6.screen15.jpg",
#         10,
#     )
# )
