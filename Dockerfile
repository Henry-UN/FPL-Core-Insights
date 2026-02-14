# FPL Core Insights API - production image
FROM python:3.11-slim

# Build-time args
ARG APP_USER=app
ARG APP_UID=1000
ARG APP_GID=1000

# Create non-root user
RUN groupadd -g ${APP_GID} ${APP_USER} \
    && useradd -m -u ${APP_UID} -g ${APP_GID} ${APP_USER}

WORKDIR /app

# Dependencies first (optimized layers)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application
COPY app/ ./app/

# Data directory (mount at runtime or copy at build)
RUN mkdir -p /app/data && chown -R ${APP_USER}:${APP_GID} /app

USER ${APP_USER}

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
