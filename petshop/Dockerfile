FROM python:3.11-slim

WORKDIR /code

# Устанавливаем системные зависимости + Python-зависимости
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir --upgrade pip==24.0 \
 && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

ENV PYTHONUNBUFFERED=1

# Gunicorn (collectstatic и migrate будут в docker-compose)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
