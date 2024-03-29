# указываем рабочую версию пайтон
FROM python:3.10
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev
#определяем рабочую директорию
RUN mkdir /fastapi_app
# перемещаемся в рабочую директорию
WORKDIR /fastapi_app
# копируем зависимости для кеширования в рабочую папку WORKDIR /fastapi_app
COPY requirements.txt .
# устанавливаем зависимости
RUN pip install -r requirements.txt
#копируем все файлы все папки проекта внуть образа
COPY . .
# Команда для запуска bash-скриптов (celery.sh)
RUN chmod a+x docker/*.sh
#запускаем uvicorn
#WORKDIR src
#срабатывает при запуске контейнера
#CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000


#запускаем фастапи в терминале
# sudo docker build . -t fastapi_app:latest
#после успешного запуска прописываем порты (до : "левый" порт, после : реальный 8000
# sudo docker run -d -p 7341:8000 fastapi_app
# возвращается хэш контейнера
# sudo docker logs <скопированный хэш>
# собираем докер-компоуз

