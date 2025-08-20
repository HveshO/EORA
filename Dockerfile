# Используем официальный Python-образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (если нужны)
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем pdm
RUN pip install --no-cache-dir pdm

# Копируем только файлы зависимостей
COPY pyproject.toml pdm.lock ./

# Устанавливаем зависимости (без dev-зависимостей)
RUN pdm install --without dev --without-hashes --frozen-lockfile

# Копируем весь проект
COPY . .

# Устанавливаем переменную окружения PYTHONPATH, чтобы src был в пути модулей
ENV PYTHONPATH=/app/src

# Запускаем main.py из src
CMD ["pdm", "run", "python", "src/main.py"]
