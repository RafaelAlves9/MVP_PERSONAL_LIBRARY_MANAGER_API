FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# Instala dependências do sistema mínimas para build de pacotes Python.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Dependências Python primeiro para aproveitar cache.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código da aplicação.
COPY . .

# Permite customizar worker/threads sem rebuild.
ENV GUNICORN_WORKERS=3 \
    GUNICORN_THREADS=2 \
    GUNICORN_TIMEOUT=120

EXPOSE 5000

RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]

