# Builder stage
FROM python:3.11-slim as builder

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /code
COPY pyproject.toml /code/

# Installing system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends  \
    build-essential \
    libpq-dev \
    && pip install --no-cache-dir --upgrade pip setuptools poetry \
    && rm -rf /var/lib/apt/lists/*

# Installing Poetry dependencies
ARG MODE
RUN poetry install $(if [ "$MODE" = "prod" ]; then echo "--no-dev"; fi) \
    && poetry cache clear . --all


# Base stage
FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Copying installed dependencies from the builder stage
COPY --from=builder /usr/local /usr/local

# Copying project source code
COPY . /code/

# Add local non-root user to avoid issue with files
ARG USERNAME=code
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && chown -R $USER_UID:$USER_GID /code

# Select internal user
USER $USERNAME