# Использование официального образа Python в качестве базового
# Мы используем python:3.11-slim, так как он меньше по размеру
FROM python:3.11-slim

# Установка переменных окружения для предотвращения буферизации вывода
# Python и для использования последней версии pip
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файла с зависимостями и их установка
# Это кэширует слой Docker, ускоряя последующие сборки
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Копирование всего остального кода приложения в контейнер
COPY . .

# Открытие порта 8000, на котором будет работать Uvicorn
EXPOSE 8000

# Команда для запуска Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]