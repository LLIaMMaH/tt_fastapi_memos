FROM python:3.11-slim

LABEL version="1.0"

ARG CONTAINER_USER=www-user
RUN useradd ${CONTAINER_USER}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt


COPY . /app/
RUN chown ${CONTAINER_USER}:${CONTAINER_USER} /app

USER ${CONTAINER_USER}

# Используем, пока тестируем наше приложение только из Dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]