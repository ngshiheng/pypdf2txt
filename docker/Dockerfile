FROM python:3.10-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5 \
    POETRY_NO_INTERACTION=1

FROM base AS builder
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root --no-interaction --no-ansi --without dev

FROM builder AS app
WORKDIR /app
COPY . /app/
CMD ["./docker/docker-entrypoint.sh"]
