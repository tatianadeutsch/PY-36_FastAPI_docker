import os
import pathlib
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi_cache import FastAPICache
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from starlette.responses import FileResponse

from src.database import async_session, session_
from src.models.models import Documents, Documents_text
from src.celery_app import scan

app = FastAPI(title="MY_FastAPI")

app_dir = os.path.dirname(__file__)  # сохраняем в отдельную переменную
path_to_doc = os.path.join(app_dir, "documents")


@app.get("/", tags=["Приветствие"])
def root_get():
    return FileResponse("src/public/index.html")


@app.post("/upload_doc", tags=["Загрузка файла, добавление записи в БД"])
async def upload_doc(file: UploadFile) -> dict:
    """
    :param file: UploadFile
    :return: dict
    """
    try:
        if file.content_type.split("/")[0] == "image":
            old_name = file.filename
            filename = "%s.%s" % (uuid.uuid4(), old_name)
            full_path = os.path.join(app_dir, "documents", filename)
            contents = await file.read()
            with open(full_path, "wb") as name_file:
                name_file.write(contents)
                # return {'message': f'file {filename} has been uploaded'}
                # Сохранение названия файла в БД
                async with async_session() as session:
                    doc = Documents(path=filename)
                    session.add(doc)
                    await session.commit()
                    return {
                        "status": "success",
                        "data": "file is saved to folder",
                        "details": None,
                    }
        return {
            "status": "error",
            "data": None,
            "details": "file format is not supported.",
        }
    except Exception:
        return {
            "status": "error",
            "data": None,
            "details": "unknown error",
        }


@app.post("/doc_delete/{doc_id}", tags=["Удаление изображения с диска и из БД"])
def delete_doc(doc_id: int):
    try:
        with session_() as session:
            query = select(Documents.path).filter(Documents.id == doc_id)
            result = session.scalar(query)
            # return result
            os.remove(os.path.join(app_dir, "documents", result))
            stmt = delete(Documents).filter(Documents.id == doc_id)
            session.execute(stmt)
            session.commit()

            return {
                "status": "success",
                "data": "Изображение успешно удалено с жесткого диска вместе с записью из БД",
                "details": None,
            }
    except:
        return {
            "status": "error",
            "data": None,
            "details": "unknown error",
        }


@app.post("/doc_analyse", tags=["Распознавание текста, его добавление в БД"])
async def doc_analyse(doc_id: int) -> dict:
    """
    :param doc_id: id файла из БД
    :return: помещает распознанные текст в БД
    """
    try:
        with session_() as session:
            query = select(Documents.path).filter(Documents.id == doc_id)
            result = session.scalar(query)
            scan.delay(os.path.join(app_dir, "documents", result), doc_id)
            return {
                "status": "success",
                "data": "Распознанный текст успешно добавлен в БД",
                "details": None,
            }
    except:
        return {
            "status": "error",
            "data": None,
            "details": "unknown error",
        }


@app.get("/get_text/{doc_id}", tags=["Вывод распознанного текста из БД"])
def get_text(doc_id: int) -> dict:
    """
    :description: API принимает id документа и возвращает распознанный текст
    :param doc_id: id из базы данных
    :return: вывод распознанного текста
    """
    try:
        with session_() as session:
            query = select(Documents_text.text).filter(Documents_text.id_doc == doc_id)
            res = session.scalar(query)
            return {
                "status": "success",
                "data": f"{res}",
                "details": None,
            }

    except:
        return {
            "status": "error",
            "data": None,
            "details": "Неизвестная ошибка",
        }


print(get_text("1"))

# @router.get("/get_text/{doc_id}")
# async def get_text(doc_id: int, session: AsyncSession = Depends(get_async_session)):
#     """По id документа получает текст обработанной картинки из таблицы Document_text\n
#        и возвращает этот текст"""
#     # проверяем есть ли запись с таким id в таблице Documents
#     query = select(Documents).filter(Documents.id == doc_id)
#     res = await session.execute(query)
#     result = res.one_or_none()
#     if result is None:
#         return {
#             "message": "error",
#              "text": f"Записи с {doc_id=}  не существует"
#         }
#
#     query = select(Documents_text.text).filter(Documents_text.id_doc == doc_id)
#     res = await session.execute(query)
#     result = res.one_or_none()
#     if result is None:
#         return {"message": "unknown",
#                  "text":   f"Документа {doc_id=} найден, но не найдена связанная с ним запись. "
#                            f"Возможно вы не задавали операцию расшифровки изображения, либо же расшифровка ещё обрабатывается."}
#     else:
#         return {"message": "success",
#                 "text": result[0]}
