# Dockerfile   (лежит в той же папке, где compose файл, или в ./bot, смотря где build указан)

FROM python:3.12-slim

WORKDIR /app

# Устанавливаем зависимости — этот слой кэшируется
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# НЕ копируем весь код — он будет монтироваться через volume
# Если хочешь, можно добавить только важные файлы, но для dev лучше volume

CMD ["python", "main.py"]